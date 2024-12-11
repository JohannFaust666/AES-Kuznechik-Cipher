# AES Kuznechik Cipher
## This is little app to ecrypt and decrypt your txt files by chosen folder using AES and Kuznechik Cipher

## Installation
To install and run the program use should install requiered python modules. You can do this running:
```shell
pip install pycryptodome pyqt5 python-dotenv
```
or 
```shell
pip install -r requirements.txt
```
Now you can run the app.

Also you need to set your .env variables:
1. ENCRYPTION_KEY - your secret key variable.
2. BACKUP_DIR - path to your backup folder.

.env example:
1. ENCRYPTION_KEY=0000000000000000000000000000000000000000000000000000000000000000
2. BACKUP_DIR=C:\Users\Alex\Desktop\Programs\Cipher\backups

## Usage
To run the app:
```shell
python main.py
```
Let's start. You'll see the main app window. You need to choose folder with your txt files you wanna ecrypt.
![image](https://github.com/user-attachments/assets/179e2c0c-770c-4aaf-814b-7986182650e6)

Then you should press "Encrypt" button. You'll see that your files are encrypted now and they're also in your backup folder.

To dencrypt them using your key press "Decrypt".

That's it. Your files are decrypted. 😊
