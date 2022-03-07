import os
import numpy
from PIL import Image, ImageDraw
import json

json_path = input("json path: ")
img_path = input("image path: ")
save_path = input("save path: ")

json_list = os.listdir(json_path)
json_list = [file for file in json_list if file.endswith(".json")]
img_list = os.listdir(img_path)
img_list = [file for file in img_list if file.endswith(".png")]

ji_list = []
for i in json_list:
    i = i.rstrip('.json')
    ji_list.append(i)

for jl in ji_list:
    x = []
    y = []
    polygon = []
    with open(json_path + jl + ".json", "r", encoding="utf8") as f:
        data = json.load(f)
        
        for a in data["annotations"]:
            i = 1
            print(a["segmentation"])
            for i in range(len(a["segmentation"][0])):
                if i%2 == 0:
                    x.append(a["segmentation"][0][i])
                else:
                    y.append(a["segmentation"][0][i])
                    
    
    for j in range(len(x)):
        polygon.append((x[j],y[j]))
    
    img = Image.open(img_path + jl+".png").convert("RGB")
    # convert to numpy (for convenience)
    img_array = numpy.asarray(img)
    
    # create new image ("1-bit pixels, black and white", (width, height), "default color")
    mask_img = Image.new('1', (img_array.shape[1], img_array.shape[0]), 0)
    ImageDraw.Draw(mask_img).polygon(polygon, outline=1, fill=1)
    mask = numpy.array(mask_img)
    
    # assemble new image (uint8: 0-255)
    new_img_array = numpy.empty(img_array.shape, dtype='uint8')

    # copy color values (RGB)
    new_img_array[:,:,:3] = img_array[:,:,:3]

    # filtering image by mask
    new_img_array[:,:,0] = new_img_array[:,:,0] * mask + 255
    new_img_array[:,:,1] = new_img_array[:,:,1] * mask + 255
    new_img_array[:,:,2] = new_img_array[:,:,2] * mask +255
    
    # back to Image from numpy
    newIm = Image.fromarray(new_img_array, "RGB")
    newIm.save(save_path+jl+".png")
    
for jl2 in ji_list:
    img = Image.open(save_path + jl2 + ".png")
    img = img.convert("RGBA")

    pixdata = img.load()

    width, height = img.size
    for y in range(height):
        for x in range(width):
            if pixdata[x, y] == (255, 255, 255, 255):
                pixdata[x, y] = (255, 255, 255, 0)

    img.save(save_path + jl2+".png", "PNG")