CC = gcc
CFLAGS = -Wall -s -fomit-frame-pointer -fno-stack-protector -D_FORTIFY_SOURCE=0 -fvisibility=hidden -fno-asynchronous-unwind-tables
LDFLAGS = -static -Wl,-s -Wl,--strip-all -Wl,--no-relax -Wl,--defsym=__ehdr_start=0
TARGET = stripped
SRC = stripped.c

all: $(TARGET) strip

$(TARGET): $(SRC)
	$(CC) $(CFLAGS) $(LDFLAGS) $(SRC) -o $(TARGET)

strip: $(TARGET)
	echo "Stripping..."
	objcopy --strip-all $(TARGET)

clean:
	rm -f $(TARGET)
