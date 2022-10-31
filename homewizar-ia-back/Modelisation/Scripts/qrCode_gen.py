import qrcode
import os

def gen_qr(data, file="qr_%d.png"):
    qrCode = qrcode.make('data here')
    type(qrcode)
    qrCode.save(file(data[3]))
    qrPath = os.path.abspath(file)
    print(qrPath)
    return qrPath

# input: data = {"id": "", "h":x, "w":x, "d": x}
# output: image file