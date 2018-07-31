from PIL import Image

def img_cut(img_path):
    img = Image.open(img_path)
    width, height = img.size
    resizedIm = img.resize((295, 413))
    resizedIm.save(img_path)

img_path = u'C:/Users/klm/Desktop/a.jpg'
img_cut(img_path)