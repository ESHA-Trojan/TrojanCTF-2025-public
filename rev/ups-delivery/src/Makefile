CC = gcc
CFLAGS = -Wall -Wextra -Wpedantic -Werror
LDFLAGS = -static
TARGET = ups
SRC = ups.c

all: $(TARGET) pack

$(TARGET): $(SRC)
	$(CC) $(CFLAGS) $(LDFLAGS) $(SRC) -o $(TARGET)

pack: $(TARGET)
	upx --best --lzma $(TARGET)

clean:
	rm -f $(TARGET)
