import cv2
import numpy as np
from PIL import Image
import exifread
import binascii
import random
from argon2 import PasswordHasher
import base64


PASSWORD_LENGTH = 12

#----------------PARAMETERS FOR ARGON HASHING-----------------
TIME_COST = 2
MEMORY_COST = 65536
PARALLELISM = 2
#------------------------------------------------------------

def seed_generator():
    master_pw = input("Enter master password: ")
    ph = PasswordHasher(time_cost=TIME_COST, memory_cost=MEMORY_COST, parallelism=PARALLELISM, hash_len=32)
    hashed_pw = ph.hash(master_pw)
    return hashed_pw

def load_image(image_path):
    image = cv2.imread(image_path)
    if image is None:
        print("Error in image.")
    return image

def extract_substring(image_array, r):
    password_bits = []
    height, width, channels = image_array.shape
    for i in range(height):
        for j in range(width):
            for z in range(channels):
                password_bits.append(format(image_array[i][j][z], '08b'))
    binary_string = ''.join(password_bits)
    byte_data = int(binary_string, 2).to_bytes((len(binary_string) + 7) // 8, byteorder="big")
    #print(byte_data)
    substring = byte_data[r:(r + PASSWORD_LENGTH)]
    
    return substring

def generatePassword(seed, substring):
    password = bytearray()
    print(substring[1])
    print(seed[1])
    for i in range(len(substring)):
        #print(substring[i], seed[i % len(seed)])
        password.append(substring[i] ^ seed[i % len(seed)])

    return password

if __name__ == "__main__" :
    #get seed from user's master password
    seed = seed_generator()
    #print(seed)
    seed = seed.split("$")[-1]
    if isinstance(seed, str):
        seed = seed.encode()
    print("seed: ", seed)

    #load image
    image_path = "images\image1.jpg"
    image = load_image(image_path)
    #print(image)

    #randomly get a substring from image to XOR with seed
    r = random.randint(0, len(image))
    substring = extract_substring(image, r)
    print("Substring:", substring)

    #seed XOR imagestring = password
    pw_unencoded = generatePassword(seed, substring)
    print("pw_encoded: ", pw_unencoded)

    #base64 encode into readable password
    password = base64.b64encode(pw_unencoded)
    print("password: ", password)


    # cv2.imshow("img", image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows