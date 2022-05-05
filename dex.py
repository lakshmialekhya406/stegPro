from PIL import Image
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
import base64
from rich import print
import sys

headerText = "M6nMjy5THr2J"

def decrypt(key, source, decode=True):
    if decode:
        source = base64.b64decode(source.encode())
    key = SHA256.new(key).digest()  
    IV = source[:AES.block_size]  
    decryptor = AES.new(key, AES.MODE_CBC, IV)
    data = decryptor.decrypt(source[AES.block_size:])  
    padding = data[-1]  
    if data[-padding:] != bytes([padding]) * padding: 
        raise ValueError("Invalid padding...")
    return data[:-padding]  

def convertToRGB(img):
	try:
		rgba_image = img
		rgba_image.load()
		background = Image.new("RGB", rgba_image.size, (255, 255, 255))
		background.paste(rgba_image, mask = rgba_image.split()[3])
		return background
	except Exception as e:
		print("Couldn't convert image to RGB")

def getPixelCount(img):
	width, height = Image.open(img).size
	return width*height

def decodeImage(image):
	try:
		pix = image.getdata()
		current_pixel = 0
		decoded=""
		while True:
			binary_value=""
			p1 = pix[current_pixel]
			p2 = pix[current_pixel+1]
			p3 = pix[current_pixel+2]
			three_pixels = [val for val in p1+p2+p3]

			for i in range(0,8):
				if three_pixels[i]%2==0:
					binary_value+="0"
				elif three_pixels[i]%2!=0:
					binary_value+="1"

			binary_value.strip()
			ascii_value = int(binary_value,2)
			decoded+=chr(ascii_value)
			current_pixel+=3

			if three_pixels[-1]%2!=0:
				break

		return decoded
	except Exception as e:
		print("An error occured")
		sys.exit()

def main():
    img = sys.argv[2]
    password = sys.argv[1]
    
    image = Image.open(img)
    cipher = decodeImage(image)

    header = cipher[:len(headerText)]

    if header.strip()!=headerText:
        print("Invalid data!")
        sys.exit(0)
    
    print()

    decrypted=""

    if password!="":
        cipher = cipher[len(headerText):]
        try:
            decrypted = decrypt(key=password.encode(),source=cipher)
        except Exception as e:
            print("Wrong password!")
            sys.exit(0)
    else:
        decrypted=cipher
    header = decrypted.decode()[:len(headerText)]

    if header!=headerText:
        print("Wrong password!")
        sys.exit(0)
    decrypted = decrypted[len(headerText):]
    print(decrypted.decode('utf-8'))


if __name__ == "__main__":
    main()