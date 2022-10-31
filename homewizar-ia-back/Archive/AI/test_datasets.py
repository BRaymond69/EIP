
from random import randint
from PIL import Image
from parse_dataset import ParseDatahubDataset

class TestParseDatahubDataset:

    def test_parse_file(self):
        parser = ParseDatahubDataset(test=True)
        
        width = randint(200, 400)
        height = randint(800, 1200)
        arr =  [[[randint(0, 255) * 3] + [255] for j in range(width)] for k in range(height)]
        exp = [[[col[0]] for col in row] for row in arr]
        img = Image.frombuffer(arr)
        with open("test.png", "wb") as im:
            img.save(im)

        got = parser.parseFile("test.png")
