import cv2
import os

# Load the original image
image_path = "mypic.jpg"
img = cv2.imread(image_path)

if img is None:
    print(f"Error: Could not load image '{image_path}'. Check the file path and format.")
    exit()

msg = input("Enter secret message: ")
password = input("Enter a passcode: ")

# Convert message to bytes (ASCII)
msg_bytes = msg.encode("utf-8")
msg_length = len(msg_bytes)

# Store message length in first 4 pixels (Red channel)
n, m = 0, 0
for i in range(4):
    img[n, m, 0] = (msg_length >> (i * 8)) & 255
    m += 1
    if m >= img.shape[1]:
        n += 1
        m = 0

# Encrypt message into the image
z = 0
for byte in msg_bytes:
    img[n, m, z] = byte
    m += 1
    if m >= img.shape[1]:
        n += 1
        m = 0
    z = (z + 1) % 3

# Save encrypted image as PNG to avoid compression
output_path = os.path.join(os.getcwd(), "encryptedImage.png")
cv2.imwrite(output_path, img)
print(f"Image saved successfully at: {output_path}")

# Save password to a file
with open("password.txt", "w") as f:
    f.write(password)

print("Encryption completed! Run 'stegodecryption.py' to decrypt the message.")
