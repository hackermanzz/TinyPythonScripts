from PIL import Image
left = int(input("Pixels from the left : "))
upper = int(input("Pixels from the top : "))
right = int(input("Pixels from the right : "))
lower = int(input("Pixels from the bottom : "))

open_img = Image.open("#ImagePath")
crop_image = open_img.crop((left,upper,right,lower))
crop_image.show()