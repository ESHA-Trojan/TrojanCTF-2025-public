#pragma once

typedef struct {
	int socket;
	int auth;
} lftpd_client_t;

/**
 * @brief Create a server on port and start listening for client
 * connections. This function blocks for the life of the server and
 * only returns when lftpd_stop() is called with the same lftpd_t.
 */
int lftpd_start(int port);

