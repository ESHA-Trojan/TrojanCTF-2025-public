package main

import (
	"bufio"
	"crypto/rand"
	"crypto/rsa"
	"crypto/sha256"
	"encoding/hex"
	"fmt"
	"os"
	"strings"
)

const (
	KEYSIZE = 2048
)

func main() {
	flag, err := readFlag()
	if err != nil {
		fmt.Println(fmt.Errorf("could not read flag: %w", err))
		return
	}

	key_alice, err := rsa.GenerateKey(rand.Reader, KEYSIZE)
	if err != nil {
		fmt.Println(fmt.Errorf("could not generate Alices key: %w", err))
		return
	}

	err = bob(&key_alice.PublicKey, flag)
	if err != nil {
		fmt.Println(err)
	}

	err = alice(key_alice)
	if err != nil {
		fmt.Println(err)
	}
}

func bob(pubkey_alice *rsa.PublicKey, flag string) error {
	plain_1 := []byte(flag[:len(flag)/2] + ",TODORANDOMSTRINGACK")

	cipher_1, err := rsa.EncryptOAEP(sha256.New(), rand.Reader, pubkey_alice, plain_1, nil)
	if err != nil {
		return fmt.Errorf("could not encrypt message 1: %w", err)
	}

	fmt.Printf("Bob says: Message 1 is %s\n", hex.EncodeToString(cipher_1))

	plain_2 := []byte("TODORANDOMSTRINGACK," + flag[len(flag)/2:])

	cipher_2, err := rsa.EncryptOAEP(sha256.New(), rand.Reader, pubkey_alice, plain_2, nil)
	if err != nil {
		return fmt.Errorf("could not encrypt message: %w", err)
	}

	fmt.Printf("Bob says: Message 2 is %s\n", hex.EncodeToString(cipher_2))

	return nil
}

func alice(key_alice *rsa.PrivateKey) error {
	fmt.Print("Receiving message 1: ")
	var cipher_1 string
	fmt.Scanln(&cipher_1)

	bytes_1, err := hex.DecodeString(cipher_1)
	if err != nil {
		return fmt.Errorf("could not decode message: %w", err)
	}

	plain_1, err := rsa.DecryptOAEP(sha256.New(), rand.Reader, key_alice, bytes_1, nil)
	if err != nil {
		return fmt.Errorf("could not decrypt message: %w", err)
	}

	ack_1 := strings.SplitAfter(string(plain_1), ",")[1]

	fmt.Printf("Alice says: Ack message 1 %s \n", ack_1)
	fmt.Print("Receiving message 2: ")

	var cipher_2 string
	fmt.Scanln(&cipher_2)

	bytes_2, err := hex.DecodeString(cipher_2)
	if err != nil {
		return fmt.Errorf("could not decode message: %w", err)
	}

	plain_2, err := rsa.DecryptOAEP(sha256.New(), rand.Reader, key_alice, bytes_2, nil)
	if err != nil {
		return fmt.Errorf("could not decrypt message: %w", err)
	}

	ack_2 := strings.SplitAfter(string(plain_2), ",")[0]
	fmt.Printf("Alice says: Ack message 2 %s \n", ack_2)

	return nil
}

func readFlag() (string, error) {
	readFile, err := os.Open("flag.txt")
	if err != nil {
		return "", err
	}
	defer readFile.Close()

	fileScanner := bufio.NewScanner(readFile)
	fileScanner.Split(bufio.ScanLines)
	for fileScanner.Scan() {
		return fileScanner.Text(), nil
	}

	return "", fmt.Errorf("flag file was empty")
}
