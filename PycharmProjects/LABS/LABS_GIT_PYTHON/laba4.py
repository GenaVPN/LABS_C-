from PIL import Image
def PIL_laba():
    with Image.open("ava.jpg") as img:
        print("Номер 1")
        x, y = img.size
        print(f"Размер изображения {x}x{y}")
        print("Номер 1 отработал")

        print("Номер 2")
        img2 = img.transpose(Image.FLIP_LEFT_RIGHT)
        img2.save("img2.png")
        print("Номер 2 отработал")

        print("Номер 3")
        img3 = Image.new("RGB", img.size)
        for i in range(img.size[0]):
            for j in range(img.size[1]):
                r,g,b = img.getpixel((i,j))
                img3.putpixel((i,j), (255 - r,255 - g,255 - b))
        img3.save("img3.png")
        print("Номер 3 отработал")



PIL_laba()
