import cv2
import numpy as np
from PIL import Image
import exifread
import binascii

PASSWORD_LENGTH = 12

def load_image(image_path):
    image = cv2.imread(image_path)
    if image is None:
        print("Error in image.")
    return image

def generate_password(image_array, r):
    password_bits = []
    height, width, channels = image_array.shape
    for i in range(height):
        for j in range(width):
            for z in range(channels):
                password_bits.append(format(image_array[i][j][z], '08b'))
    binary_string = ''.join(password_bits)
    byte_data = int(binary_string, 2).to_bytes((len(binary_string) + 7) // 8, byteorder="big")
    print(byte_data)
    password_data = byte_data[r:(r + PASSWORD_LENGTH)]
    print("password_data: ", password_data)
    ascii = binascii.b2a_uu(password_data).decode().strip()
    return ascii

if __name__ == "__main__" :
    image_path = "images\image1.jpg"
    image = load_image(image_path)
    r = 100
    password = generate_password(image, r)
    print("Password: ", password)

    # cv2.imshow("img", image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows