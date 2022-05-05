from PIL import Image
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto import Random
import base64
from rich import print
import sys

headerText = "M6nMjy5THr2J"

def encrypt(key, source, encode=True):
    key = SHA256.new(key).digest()  
    IV = Random.new().read(AES.block_size)  
    encryptor = AES.new(key, AES.MODE_CBC, IV)
    padding = AES.block_size - len(source) % AES.block_size  
    source += bytes([padding]) * padding  
    data = IV + encryptor.encrypt(source)  
    return base64.b64encode(data).decode() if encode else data

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

def encodeImage(image,message,filename):
	
	try:
		width, height = image.size
		pix = image.getdata()

		current_pixel = 0
		tmp=0
		x=0
		y=0
		for ch in message:
			binary_value = format(ord(ch), '08b')
			
			p1 = pix[current_pixel]
			p2 = pix[current_pixel+1]
			p3 = pix[current_pixel+2]

			three_pixels = [val for val in p1+p2+p3]

			for i in range(0,8):
				current_bit = binary_value[i]

				if current_bit == '0':
					if three_pixels[i]%2!=0:
						three_pixels[i]= three_pixels[i]-1 if three_pixels[i]==255 else three_pixels[i]+1
				elif current_bit == '1':
					if three_pixels[i]%2==0:
						three_pixels[i]= three_pixels[i]-1 if three_pixels[i]==255 else three_pixels[i]+1

			current_pixel+=3
			tmp+=1

			if(tmp==len(message)):
				if three_pixels[-1]%2==0:
					three_pixels[-1]= three_pixels[-1]-1 if three_pixels[-1]==255 else three_pixels[-1]+1
			else:
				if three_pixels[-1]%2!=0:
					three_pixels[-1]= three_pixels[-1]-1 if three_pixels[-1]==255 else three_pixels[-1]+1

			three_pixels = tuple(three_pixels)
			
			st=0
			end=3

			for i in range(0,3):
				image.putpixel((x,y), three_pixels[st:end])
				st+=3
				end+=3

				if (x == width - 1):
					x = 0
					y += 1
				else:
					x += 1
		name = list(filename.split('.')[0].split('\\'))
		encoded_filename = "C:\\Users\\dell\\Desktop\\" + name[-1] + "-enc.png"
		image.save(encoded_filename)
		print(encoded_filename)

	except Exception as e:
		print("An error occured")

def main():
    img = sys.argv[3]
    message = sys.argv[1]
    password = sys.argv[2]
    cipher = ""

    message = headerText + message
    if((len(message)+len(headerText))*3> getPixelCount(img)):
        raise Exception("Given message is too long to be encoded in the image.")

    if password!="":
        cipher = encrypt(key=password.encode(),source=message.encode())
        cipher = headerText + cipher
    else:
        cipher = message
    image = Image.open(img)
    if image.mode != 'RGB':
        image = convertToRGB(image)

    newimg = image.copy()
    encodeImage(image=newimg,message=cipher,filename=image.filename)


if __name__ == "__main__":
    main()