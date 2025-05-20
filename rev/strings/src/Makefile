CC = gcc
CFLAGS = -Wall -Wextra -Wpedantic -Werror
LDFLAGS = -static
TARGET = strings
SRC = strings.c

all: $(TARGET)

$(TARGET): $(SRC)
	$(CC) $(CFLAGS) $(LDFLAGS) $(SRC) -o $(TARGET)

clean:
	rm -f $(TARGET)
