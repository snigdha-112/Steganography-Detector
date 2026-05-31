from stegano import lsb
secret_message = "This is  a hidden message for cnn dectective!"
secert_image = lsb.hide("D:/stegoproject/flower.jpg", secret_message)
secert_image.save("D:/stegoproject/stego_flower.png")
print("success! 'stego_flower.png' has been created.")
