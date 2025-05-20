#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <stdarg.h>
#include <stdbool.h>
#include <unistd.h>
#include <ctype.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <dirent.h>
#include <errno.h>
#include <sys/stat.h>
#include <pthread.h>

#include "lftpd.h"

#include "private/lftpd_status.h"
#include "private/lftpd_inet.h"
#include "private/lftpd_log.h"
#include "private/lftpd_string.h"
#include "private/lftpd_io.h"

// https://tools.ietf.org/html/rfc959
// https://tools.ietf.org/html/rfc2389#section-2.2
// https://tools.ietf.org/html/rfc3659
// https://tools.ietf.org/html/rfc5797
// https://tools.ietf.org/html/rfc2428#section-3 EPSV
// https://en.wikipedia.org/wiki/List_of_FTP_commands

typedef struct {
	char *command;
	int (*handler) (lftpd_client_t* client, const char* arg);
} command_t;

static int cmd_cwd(lftpd_client_t* client, const char* arg);
static int cmd_dele(lftpd_client_t* client, const char* arg);
static int cmd_epsv(lftpd_client_t* client, const char* arg);
static int cmd_feat(lftpd_client_t* client, const char* arg);
static int cmd_list(lftpd_client_t* client, const char* arg);
static int cmd_nlst(lftpd_client_t* client, const char* arg);
static int cmd_noop(lftpd_client_t* client, const char* arg);
static int cmd_pass(lftpd_client_t* client, const char* arg);
static int cmd_pasv(lftpd_client_t* client, const char* arg);
static int cmd_pwd(lftpd_client_t* client, const char* arg);
static int cmd_quit(lftpd_client_t* client, const char* arg);
static int cmd_retr(lftpd_client_t* client, const char* arg);
static int cmd_size(lftpd_client_t* client, const char* arg);
static int cmd_stor(lftpd_client_t* client, const char* arg);
static int cmd_syst(lftpd_client_t* client, const char* arg);
static int cmd_type(lftpd_client_t* client, const char* arg);
static int cmd_user(lftpd_client_t* client, const char* arg);

static int cmd_loginrequired(lftpd_client_t* client, const char* arg);

static bool check_username(const char* username);
static bool check_password(const char* password);

// respond to most commands saying they're not logged in
static command_t commands[] = {
	{ "CWD", cmd_loginrequired },
	{ "DELE", cmd_loginrequired },
	{ "EPSV", cmd_loginrequired },
	{ "FEAT", cmd_feat },
	{ "LIST", cmd_loginrequired },
	{ "NLST", cmd_loginrequired },
	{ "NOOP", cmd_noop },
	{ "PASS", cmd_pass },
	{ "PASV", cmd_loginrequired },
	{ "PWD", cmd_loginrequired },
	{ "QUIT", cmd_quit },
	{ "RETR", cmd_loginrequired },
	{ "SIZE", cmd_loginrequired },
	{ "STOR", cmd_loginrequired },
	{ "SYST", cmd_syst },
	{ "TYPE", cmd_type },
	{ "USER", cmd_user },
	{ NULL, NULL },
};

static int send_response(int socket, int code, bool include_code,
		bool multiline_start, const char* format, ...) {
	va_list args;
	va_start(args, format);
	char* message = NULL;
	int err = vasprintf(&message, format, args);
	va_end(args);
	if (err < 0) {
		return -1;
	}

	char* response = NULL;
	if (include_code) {
		if (multiline_start) {
			err = asprintf(&response, "%d-%s%s", code, message, CRLF);
		}
		else {
			err = asprintf(&response, "%d %s%s", code, message, CRLF);
		}
	}
	else {
		err = asprintf(&response, "%s%s", message, CRLF);
	}
	free(message);
	if (err < 0) {
		return -1;
	}

	err = lftpd_inet_write_string(socket, response);
	free(response);
	return err;
}

#define send_simple_response(socket, code, format, ...) send_response(socket, code, true, false, format, ##__VA_ARGS__)

#define send_multiline_response_begin(socket, code, format, ...) send_response(socket, code, true, true, format, ##__VA_ARGS__)

#define send_multiline_response_line(socket, format, ...) send_response(socket, 0, false, false, format, ##__VA_ARGS__)

#define send_multiline_response_end(socket, code, format, ...) send_response(socket, code, true, false, format, ##__VA_ARGS__)


static int cmd_feat(lftpd_client_t* client, const char* arg) {
	send_multiline_response_begin(client->socket, 211, STATUS_211);
	send_multiline_response_line(client->socket, "EPSV");
	send_multiline_response_line(client->socket, "PASV");
	send_multiline_response_line(client->socket, "SIZE");
	send_multiline_response_line(client->socket, "NLST");
	send_multiline_response_end(client->socket, 211, STATUS_211);
	return 0;
}

static int cmd_noop(lftpd_client_t* client, const char* arg) {
	send_simple_response(client->socket, 200, STATUS_200);
	return 0;
}

static int cmd_pass(lftpd_client_t* client, const char* arg) {
	if (client->auth == 1 && check_password(arg)) {
		client->auth = 2;
		send_simple_response(client->socket, 230, STATUS_230);
	}
	else {
		send_simple_response(client->socket, 530, STATUS_530);
	}
	return 0;
}

static int cmd_quit(lftpd_client_t* client, const char* arg) {
	send_simple_response(client->socket, 221, STATUS_221);
	return -1;
}

static int cmd_syst(lftpd_client_t* client, const char* arg) {
	send_simple_response(client->socket, 215, "UNIX Type: L8");
	return 0;
}

static int cmd_type(lftpd_client_t* client, const char* arg) {
	send_simple_response(client->socket, 200, STATUS_200);
	return 0;
}

static int cmd_user(lftpd_client_t* client, const char* arg) {
	if (check_username(arg)) {
		client->auth = 1;
		send_simple_response(client->socket, 331, STATUS_331);
	}
	else {
		send_simple_response(client->socket, 530, STATUS_530);
	}
	return 0;
}

static int cmd_loginrequired(lftpd_client_t* client, const char* arg) {
	send_simple_response(client->socket, 530, STATUS_530);
	return 0;
}

static bool slow_str_cmp(const char* a, const char* b) {
	while (*a && *a == *b) {
		++a; ++b;
		usleep(0.2 * 1000 * 1000); // 0.2 seconds
	}
	return *a == *b;
}

static bool check_username(const char* username) {
	lftpd_log_info("username guess: %s", username);
	return slow_str_cmp(username, "gRamP5");
}

static bool check_password(const char* password) {
	lftpd_log_info("password guess: %s", password);
	return slow_str_cmp(password, "iS_C0ol");
}

static int handle_control_channel(lftpd_client_t* client) {
	int err = send_simple_response(client->socket, 220, STATUS_220);
	if (err != 0) {
		lftpd_log_error("error sending welcome message");
		goto cleanup;
	}

	size_t read_buffer_len = 512;
	char* read_buffer = malloc(read_buffer_len);
	while (err == 0) {
		int line_len = lftpd_inet_read_line(client->socket, read_buffer, read_buffer_len);
		if (line_len != 0) {
			lftpd_log_error("error reading next command");
			goto cleanup;
		}

		// find the index of the first space
		int index;
		char* p = strchr(read_buffer, ' ');
		if (p != NULL) {
			index = p - read_buffer;
		}
		// if no space, use the whole string
		else {
			index = strlen(read_buffer);
		}

		// if the index is 5 or greater the command is too long
		if (index >= 5) {
			err = send_simple_response(client->socket, 500, STATUS_500);
			continue;
		}

		// copy the command into a temporary buffer
		char command_tmp[4 + 1];
		memset(command_tmp, 0, sizeof(command_tmp));
		memcpy(command_tmp, read_buffer, index);

		// upper case the command
		for (int i = 0; command_tmp[i]; i++) {
			command_tmp[i] = (char) toupper((int) command_tmp[i]);
		}

		// see if we have a matching function for the command, and if
		// so, dispatch it
		bool matched = false;
		for (int i = 0; commands[i].command; i++) {
			if (strcmp(commands[i].command, command_tmp) == 0) {
				char* arg = NULL;
				if (index < strlen(read_buffer)) {
					arg = strdup(read_buffer + index + 1);
					arg = lftpd_string_trim(arg);
				}
				err = commands[i].handler(client, arg);
				free(arg);
				matched = true;
				break;
			}
		}
		if (!matched) {
			send_simple_response(client->socket, 502, STATUS_502);
		}
	}

	cleanup:

	close(client->socket);
	free(client);
	
	return 0;
}

int lftpd_start(int port) {
	int server_socket = lftpd_inet_listen(port);

	if (server_socket < 0) {
		lftpd_log_error("error creating listener");
		return -1;
	}

	struct sockaddr_in6 server_addr;
	socklen_t server_addr_len = sizeof(struct sockaddr_in6);
	int err = getsockname(server_socket, (struct sockaddr*) &server_addr, &server_addr_len);
	if (err != 0) {
		lftpd_log_error("error getting server IP info");
	}
	else {
		char ip[INET6_ADDRSTRLEN];
		inet_ntop(AF_INET6, &server_addr.sin6_addr, ip, INET6_ADDRSTRLEN);
		int port = lftpd_inet_get_socket_port(server_socket);
		lftpd_log_info("listening on [%s]:%d...", ip, port);
	}

	while (true) {
		// lftpd_log_info("waiting for connection...");

		int client_socket = accept(server_socket, NULL, NULL);
		if (client_socket < 0) {
			lftpd_log_error("error accepting client socket");
			break;
		}

		struct sockaddr_in6 client_addr;
		socklen_t client_addr_len = sizeof(struct sockaddr_in6);
		int err = getpeername(client_socket, (struct sockaddr*) &client_addr, &client_addr_len);
		if (err != 0) {
			lftpd_log_error("error getting client IP info");
			lftpd_log_info("connection received...");
		}
		else {
			char ip[INET6_ADDRSTRLEN];
			inet_ntop(AF_INET6, &client_addr.sin6_addr, ip, INET6_ADDRSTRLEN);
			int port = lftpd_inet_get_socket_port(client_socket);
			lftpd_log_info("connection received from [%s]:%d...", ip, port);
		}

		lftpd_client_t *client = malloc(sizeof *client);
		if (!client) {
			lftpd_log_error("malloc");
			close(client_socket);
			continue;
		}
		client->socket    = client_socket;
		client->auth        = 0;

		pthread_t thread;
		if (pthread_create(&thread, NULL,
						(void*(*)(void*))handle_control_channel,
						client) != 0)
		{
			lftpd_log_error("error creating thread for client");
			close(client->socket);
			free(client);
			continue;
		}

		// detach and let the thread clean up
		pthread_detach(thread);
	}

	close(server_socket);

	return 0;
}

int main( int argc, char *argv[] ) {
	setbuf(stdout, NULL);
	lftpd_start(2121);
}

