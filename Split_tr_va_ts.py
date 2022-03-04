import os
import json
import funcy
from sklearn.model_selection import train_test_split

json_path = input("Enter json path: ")
json_list = os.listdir(json_path)

ratio_train = float(input("Train ratio: "))
ratio_valid = float(input("Valid ratio: "))
ratio_test = float(input("Test ratio: "))

def save_coco(file, info, licenses, images, annotations, categories):
    with open(file, 'wt', encoding='UTF-8') as coco:
        json.dump({ 'info': info, 'licenses': licenses, 'images': images, 
            'annotations': annotations, 'categories': categories}, coco, indent=2, sort_keys=True)

def filter_annotations(annotations, images):
    image_ids = funcy.lmap(lambda i: int(i['id']), images)
    return funcy.lfilter(lambda a: int(a['image_id']) in image_ids, annotations)

def main():
    with open(json_path + json_list[0], 'rt', encoding='UTF-8') as annotations:
        coco = json.load(annotations)
        print("load success")
        info = coco['info']
        licenses = coco['licenses']
        images = coco['images']
        annotations = coco['annotations']
        categories = coco['categories']

        number_of_images = len(images)

        images_with_annotations = funcy.lmap(lambda a: int(a['image_id']), annotations)

        if annotations:
            images = funcy.lremove(lambda i: i['id'] not in images_with_annotations, images)

        train_before, test = train_test_split(
            images, test_size=ratio_test)

        ratio_remaining = 1 - ratio_test
        ratio_valid_adjusted = ratio_valid / ratio_remaining

        train_after, valid = train_test_split(
            train_before, test_size=ratio_valid_adjusted)

        save_coco('train', info, licenses, train_after, filter_annotations(annotations, train_after), categories)
        print("complete train")
        save_coco('test', info, licenses, test, filter_annotations(annotations, test), categories)
        print("complete test")
        save_coco('valid', info, licenses, valid, filter_annotations(annotations, valid), categories)
        print("complete valid")
        
        print("Saved {} entries in {} and {} in {} and {} in {}".format(len(train_after), 'train', len(test), 'test', len(valid), 'valid'))


if __name__ == "__main__":
    main()
