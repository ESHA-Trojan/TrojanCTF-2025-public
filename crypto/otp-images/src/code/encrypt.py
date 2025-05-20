import os
import numpy as np
import cv2
import secrets

#get the file path
base_path = os.path.abspath(__file__)
base_path = base_path.replace("encrypt.py", "")

image_shape = (512, 512, 3)
key = ""
secret_key_file = "secret_key"
if not os.path.exists(base_path + secret_key_file + ".npy"):
	key = np.array([secrets.randbelow(256) for _ in range(np.prod(image_shape))], dtype=np.uint8).reshape(image_shape)
	np.save(base_path + secret_key_file, key)
else:
	key = np.load(base_path + secret_key_file + ".npy")

def encrypt_image(image_name):
	image = cv2.imread(base_path + image_name + ".png")
	enc_image = cv2.bitwise_xor(image, key)
	cv2.imwrite(base_path + image_name + ".enc.png", enc_image)

def decrypt_image(image_name):
	image = cv2.imread(base_path + image_name + ".enc.png")
	dec_image = cv2.bitwise_xor(image, key)
	cv2.imwrite(base_path + image_name + ".dec.png", dec_image)

def main():
	encrypt_image("flag")
	decrypt_image("flag")
	encrypt_image("stars")
	decrypt_image("stars")
 
if __name__ == "__main__":
	main()
     