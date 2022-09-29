from convert import Convert
from PIL import Image

if __name__ == "__main__":
    images = [r"assets/hanging_lamp.jpg", r"assets/pear.jpg", r"assets/weird_dog.jpg"]
    for path in images:
        print(Convert(Image.open(path), 80).toText())