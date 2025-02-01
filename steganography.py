from PIL import Image

class Steganography:
    def __init__(self, image_path, data=None):
        self.image_path = image_path
        self.data = data
        self.image = Image.open(self.image_path, 'r')
        self.newimg = self.image.copy()

    # Convert encoding data into 8-bit binary
    # form using ASCII value of characters
    def genData(self):
        newd = [format(ord(i), '08b') for i in self.data]
        return newd

    # Pixels are modified according to the
    # 8-bit binary data and finally returned
    def modPix(self, pix):
        datalist = self.genData()
        lendata = len(datalist)
        imdata = iter(pix)

        for i in range(lendata):
            # Extracting 3 pixels at a time
            pix = [value for value in imdata.__next__()[:3] +
                                    imdata.__next__()[:3] +
                                    imdata.__next__()[:3]]

            # Pixel value should be made
            # odd for 1 and even for 0
            for j in range(0, 8):
                if (datalist[i][j] == '0' and pix[j] % 2 != 0):
                    pix[j] -= 1
                elif (datalist[i][j] == '1' and pix[j] % 2 == 0):
                    if (pix[j] != 0):
                        pix[j] -= 1
                    else:
                        pix[j] += 1

            # Eighth pixel of every set tells
            # whether to stop to read further.
            if (i == lendata - 1):
                if (pix[-1] % 2 == 0):
                    if (pix[-1] != 0):
                        pix[-1] -= 1
                    else:
                        pix[-1] += 1
            else:
                if (pix[-1] % 2 != 0):
                    pix[-1] -= 1

            pix = tuple(pix)
            yield pix[0:3]
            yield pix[3:6]
            yield pix[6:9]

    def encode_enc(self):
        w = self.newimg.size[0]
        (x, y) = (0, 0)

        for pixel in self.modPix(self.newimg.getdata()):
            # Putting modified pixels in the new image
            self.newimg.putpixel((x, y), pixel)
            if (x == w - 1):
                x = 0
                y += 1
            else:
                x += 1

    def encode(self, output_path):
        self.encode_enc()
        self.newimg.save(output_path)

    def decode(self):
        imgdata = iter(self.image.getdata())
        data = ''

        while True:
            pixels = [value for value in imgdata.__next__()[:3] +
                                    imgdata.__next__()[:3] +
                                    imgdata.__next__()[:3]]

            # string of binary data
            binstr = ''.join('1' if i % 2 else '0' for i in pixels[:8])
            data += chr(int(binstr, 2))
            if (pixels[-1] % 2 != 0):
                return data

# Example usage
if __name__ == '__main__':
    stego = Steganography('output.png', 'Hello World!')
    # stego.encode("output.jpg")

    decoded_data = stego.decode()
    print("Decoded Data:", decoded_data)
