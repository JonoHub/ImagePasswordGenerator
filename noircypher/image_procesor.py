import cv2
from PIL import Image
from argon2.low_level import hash_secret_raw, Type
from argon2 import PasswordHasher
import base64
import hashlib


PASSWORD_LENGTH = 12

#----------------PARAMETERS FOR ARGON HASHING-----------------
TIME_COST = 2
MEMORY_COST = 65536
PARALLELISM = 2
ph = PasswordHasher(time_cost=TIME_COST, memory_cost=MEMORY_COST, parallelism=PARALLELISM, hash_len=32)
#------------------------------------------------------------

#as of now, I dont think this is safe cuz password = seed XOR substring
#so, the hacker doesnt need the master password to get the service password
#but how would the intruder get the seed, since its not stored. its only derived from the master password.
#Q.How can the hacker get the seed without the master password. 

#r needs to be derived from master pw also

def seed_generator(master_pw):

    salt = hashlib.sha256(master_pw.encode()).digest()[:16]

    seed = hash_secret_raw(
        secret=master_pw.encode(),
        salt = salt,
        time_cost=TIME_COST,
        memory_cost=MEMORY_COST,
        parallelism=PARALLELISM,
        hash_len=32,
        type=Type.ID
    )

    # hashed_pw = ph.hash(master_pw)
    # hashed_pw = hashed_pw.split("$")[-1]
    if isinstance(seed, str):
        seed = seed.encode()
    return seed

def load_image(image_path):
    image = cv2.imread(image_path)
    if image is None:
        print("Error in image.")
    return image

def generate_r(image, seed):
    to_hash = image.tobytes() + seed
    hash_digest = hashlib.sha256(to_hash).digest()
    image_length = len(image)
    r = int.from_bytes(hash_digest) % image_length
    print("r/image length: ", r, "/", image_length)
    return r

def extract_substring(image_array, r):
    byte_data = image_array.tobytes()
    substring = byte_data[r:(r + PASSWORD_LENGTH)]
    return substring

def generatePassword(seed, substring):
    password = bytearray()
    for i in range(len(substring)):
        #print(substring[i], seed[i % len(seed)])
        password.append(substring[i] ^ seed[i % len(seed)])

    return password

if __name__ == "__main__" :
    #master_pw = input("Enter master password: ")
    master_pw = "patinhovai1234"

    #get seed from user's master password
    seed = seed_generator(master_pw)
    print("seed: ", seed)

    #load image
    image_path = "images\image2.jpg"
    image = load_image(image_path)
    #print(image)

    #randomly get a substring from image to XOR with seed
    r = generate_r(image, master_pw.encode())
    substring = extract_substring(image, r)
    print("Substring:", substring)

    #seed XOR imagestring = password
    password = generatePassword(seed, substring)
    print("pw_encoded: ", password)

    #base64 encode into readable password
    password = base64.b64encode(password).decode()
    print("password: ", password)


    # cv2.imshow("img", image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows