import cv2
import os

# Define image path
image_path = os.path.join(os.getcwd(), "encryptedImage.png")

# Load the encrypted image
if not os.path.exists(image_path):
    print(f"Error: Could not find encrypted image at '{image_path}'. Make sure encryption was done correctly.")
    exit()

img = cv2.imread(image_path)

if img is None:
    print("Error: Unable to read the encrypted image. It might be corrupted.")
    exit()

# Load the stored password
password_path = os.path.join(os.getcwd(), "password.txt")

if not os.path.exists(password_path):
    print("Error: Password file not found. Encryption might not have been completed.")
    exit()

with open(password_path, "r") as f:
    stored_password = f.read().strip()

# User enters password for decryption
pas = input("Enter passcode for decryption: ")

if pas == stored_password:
    # Read message length from the first 4 pixels
    msg_length = 0
    n, m = 0, 0
    for i in range(4):
        msg_length += img[n, m, 0] << (i * 8)
        m += 1
        if m >= img.shape[1]:
            n += 1
            m = 0

    # Decrypt message from the image
    message_bytes = bytearray()
    z = 0
    for _ in range(msg_length):
        message_bytes.append(img[n, m, z])
        m += 1
        if m >= img.shape[1]:
            n += 1
            m = 0
        z = (z + 1) % 3

    message = message_bytes.decode("utf-8")
    print("Decryption successful! Message:", message)
else:
    print("YOU ARE NOT AUTHORIZED")
