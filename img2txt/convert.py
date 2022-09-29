from PIL import Image


class Convert:
    """
    Main class of this module. Initiate the class with an image object from PIL, with the second argument being the output's width.
    Use the toText method to return the image's string form
    Examples of its usage can be seen in test.py
    """

    def __init__(self, image: Image.Image, width: int):
        """
        Main class of this module. Initiate the class with an image object from PIL, with the second argument being the output's width.
        Use the toText method to return the image's string form
        Examples of its usage can be seen in test.py
        :param image: PIL.Image.Image. The image to convert. Must be PIL.Image.Image
        :param width: int. The width of the output
        """
        self.gradient = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:," + '"' + "^`'. "
        self.image = image.convert("L")
        self.width = width

    def setGradient(self, newgradient: str):
        """
        Set a new, custom gradient
        :param newgradient: str
        :return: None
        """
        self.gradient = newgradient

    def resetGradient(self):
        """
        Sets a new gradient. No arguments nor return
        :return: None
        """
        self.gradient = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:," + '"' + "^`'. "

    def toText(self, resize=True) -> str:
        """
        Returns the text version of this.image.
        :param resize: Bool=True. True if the output is to be resized to match self.width
        :return: str
        """
        output = ""
        width, height = self.image.size
        ratio = width//self.width if resize else 1
        gradientLength = len(self.gradient) - 1
        for y in range(0, height, ratio):
            for x in range(0, width, ratio):
                color = self.image.getpixel((x, y))
                output += self.gradient[round((color / 255) * gradientLength)]
            output += "\n"
        return output
