import os
import json
import shutil
import numpy

from collections import OrderedDict
from PIL import Image, ImageDraw

def copyji(json_path, json_list, img_path, img_list, save_json, save_img):
    print("\nData preprocessing . . .")
    coco_group = OrderedDict()
    info = OrderedDict()
    licenses = OrderedDict()
    categories = OrderedDict()
    images = OrderedDict()
    annotations = OrderedDict()

    info["year"] = None
    info["version"] = None
    info["description"] = None
    info["contributor"] = None
    info["url"] = None
    info["date_created"] = None

    licenses["id"] = 1
    licenses["url"] = None
    licenses["name"] = None

    categories=[
            {
                "id": 1,
                "name": "경계석",
                "subcategory": ""
            }
        ]
    images = "{}"
    annotations = "{}"


    coco_group["info"] = info
    coco_group["licenses"] = [licenses]
    coco_group["categories"] = categories
    coco_group["images"] = [images]
    coco_group["annotations"] = [annotations]

    img_list = []
    ann_list = []

    ji_list = []
    for i in json_list:
        i = i.rstrip('.json')
        ji_list.append(i)
        
    for jl in ji_list:
        with open(json_path + "//" + jl + '.json', 'r', encoding='utf8') as f:
            data = json.load(f)
            
            if len(data["annotations"]) >= 2:
                for a in data['images']:
                    img_list.append(a)
                for b in data['annotations']:
                    ann_list.append(b)
            
                for i in range(len(data["annotations"])):
                    images=img_list
                    annotations=ann_list[i]

                    coco_group["images"] = images
                    coco_group["annotations"] = [annotations] 

                    shutil.copy2(img_path + "//" + jl + '.png', save_img + '//' + jl + "_" + str(i+1) + '.png')

                    with open(save_json + "//" + jl + "_" + str(i+1) + '.json', 'w+', encoding='utf8') as make_file:
                            json.dump(coco_group, make_file, ensure_ascii=False, indent="\t")
            else:
                shutil.copy2(img_path + "//" + jl + '.png', save_img + '//' + jl + '.png')
                with open(save_json + "//" + jl + '.json', 'w+', encoding='utf8') as make_file:
                        json.dump(data, make_file, ensure_ascii=False, indent="\t")
                        
    rmbg(save_json, save_img, save_img)

def rmbg(json_path, img_path, save_path):
    print("\nData cropping . . . ")
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
        with open(json_path + "//" + jl + ".json", "r", encoding="utf8") as f:
            data = json.load(f)
            
        for a in data["annotations"]:
            i = 0
            for i in range(len(a["segmentation"][0])):
                if i%2 == 0:
                    x.append(a["segmentation"][0][i])
                else:
                    y.append(a["segmentation"][0][i])
                        
        for b in data["images"]:
            b["file_name"] = jl + ".png"
        for j in range(len(x)):
            polygon.append((x[j],y[j])) # Save x and y coordinate values in a tuple form.
        
        img = Image.open(img_path + "//" + jl +".png").convert("RGB")
        # convert to numpy (for convenience)
        img_array = numpy.asarray(img)
        
        # create new image (Background color - black)
        mask_img = Image.new('1', (img_array.shape[1], img_array.shape[0]), 0)
        ImageDraw.Draw(mask_img).polygon(polygon, outline=1, fill=1)
        mask = numpy.array(mask_img)
        
        # assemble new image
        new_img_array = numpy.empty(img_array.shape, dtype='uint8')

        # copy color values (RGB)
        new_img_array[:,:,:3] = img_array[:,:,:3]

        # filtering image by mask(Baclground color - white => to change Transparent background)
        new_img_array[:,:,0] = new_img_array[:,:,0] * mask + 255
        new_img_array[:,:,1] = new_img_array[:,:,1] * mask + 255
        new_img_array[:,:,2] = new_img_array[:,:,2] * mask + 255
        
        # back to Image from numpy
        newIm = Image.fromarray(new_img_array, "RGB")
        newIm.save(save_path + "//" + jl + ".png")
        
        with open(json_path + "//" + jl + '.json', 'w+', encoding='utf8') as make_file:
            json.dump(data, make_file, ensure_ascii=False, indent="\t")
    print("\nRemoving background . . .")    
    for jl2 in ji_list:
        img = Image.open(save_path + "//" + jl2 + ".png")
        img = img.convert("RGBA")

        pixdata = img.load()

        width, height = img.size
        for y in range(height):
            for x in range(width):
                if pixdata[x, y] == (255, 255, 255, 255):
                    pixdata[x, y] = (255, 255, 255, 0)

        img.save(save_path + "//" + jl2+".png", "PNG")
        
    print("\nDone!")
def main():
    try:
        while True:
            num = int(input("\n1. Start Data cropping\n2. End program\nEnter number: "))
            if num == 2:
                print("")
                break
            elif num == 1:
                json_path = input("\nEnter json path: ")       
                json_list = os.listdir(json_path)
                json_list = [file for file in json_list if file.endswith(".json")]
                if json_list == []:
                    print("No json files.")
                    json_path = input("\nEnter json path: ")
                    json_list = os.listdir(json_path)
                    json_list = [file for file in json_list if file.endswith(".json")]
                    
                img_path = input("Enter image path: ")
                img_list = os.listdir(img_path)
                img_list = [file for file in img_list if file.endswith(".png")]
                if img_list == []:
                    print("No image files.")
                    img_path = input("\nEnter image path: ")
                    img_list = os.listdir(img_path)
                    img_list = [file for file in img_list if file.endswith(".png")]
                
                save_json = input("Enter save json path: ")    
                save_img = input("Enter save image path: ")
                
                copyji(json_path, json_list, img_path, img_list, save_json, save_img)
            else:
                print("\nYou entered wrong number. Retry!!")   
             
    except FileNotFoundError:
        print("\nWrong path. Please enter the exact path.")
    except ValueError:
        print("\nWrong input. Please enter only 1 or 2.")
    except OSError:
        print("\n Invalid input. Retry!")
if __name__ == "__main__":
    print("[2022 AI Data crop program]")
    main()