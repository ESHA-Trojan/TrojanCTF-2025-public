import os
import cv2

base_path = os.path.abspath(__file__)
base_path = base_path.replace("solution.py", "")

flag_enc = cv2.imread(base_path + "flag.enc.png")
stars_enc = cv2.imread(base_path + "stars.enc.png")

xor_img = cv2.bitwise_xor(flag_enc, stars_enc)
cv2.imwrite(base_path + "flag.xor.png", xor_img)