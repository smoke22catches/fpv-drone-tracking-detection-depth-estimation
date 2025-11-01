import argparse
import os
import shutil
import xml.etree.ElementTree as ET

def convert_xml_to_coco_format(annotation_file: str) -> str:
    tree = ET.parse(annotation_file)
    root = tree.getroot()
    obj = root.find('object')
    xmin = int(obj.find('bndbox').find('xmin').text)
    ymin = int(obj.find('bndbox').find('ymin').text)
    xmax = int(obj.find('bndbox').find('xmax').text)
    ymax = int(obj.find('bndbox').find('ymax').text)

    size = root.find('size')
    image_width = int(size.find('width').text)
    image_height = int(size.find('height').text)

    center_x = (xmin + xmax) / 2 / image_width
    center_y = (ymin + ymax) / 2 / image_height
    width = (xmax - xmin) / image_width
    height = (ymax - ymin) / image_height

    return f"0 {center_x} {center_y} {width} {height}"

def main(train_input: str, annotation_input: str, train_output: str) -> None:
    # check if folders exist and create them if they don't
    if not os.path.exists(train_output):
        os.makedirs(train_output)

    if not os.path.exists(os.path.join(train_output, 'images')):
        os.makedirs(os.path.join(train_output, 'images'))

    if not os.path.exists(os.path.join(train_output, 'images', 'train')):
        os.makedirs(os.path.join(train_output, 'images', 'train'))

    if not os.path.exists(os.path.join(train_output, 'images', 'val')):
        os.makedirs(os.path.join(train_output, 'images', 'val'))

    if not os.path.exists(os.path.join(train_output, 'labels')):
        os.makedirs(os.path.join(train_output, 'labels'))

    if not os.path.exists(os.path.join(train_output, 'labels', 'train')):
        os.makedirs(os.path.join(train_output, 'labels', 'train'))

    if not os.path.exists(os.path.join(train_output, 'labels', 'val')):
        os.makedirs(os.path.join(train_output, 'labels', 'val'))

    # split train_files into train and val in 80/20 ratio
    train_files = os.listdir(train_input)
    train_files_len = len(train_files)
    train_files_train = train_files[:int(train_files_len * 0.8)]
    train_files_val = train_files[int(train_files_len * 0.8):]

    # Iterate over all files in train_input folder and copy them to train_output folder
    for filename in train_files_train:
        src_file = os.path.join(train_input, filename)
        dst_file = os.path.join(train_output, 'images', 'train', filename)
        shutil.copy2(src_file, dst_file)
        annotation_file = os.path.join(annotation_input, filename.replace('.jpg', '.xml'))
        annotation_content = convert_xml_to_coco_format(annotation_file)
        with open(os.path.join(train_output, 'labels', 'train',filename.replace('.jpg', '.txt')), 'w') as f:
            f.write(annotation_content)

    for filename in train_files_val:
        src_file = os.path.join(train_input, filename)
        dst_file = os.path.join(train_output, 'images', 'val', filename)
        shutil.copy2(src_file, dst_file)
        annotation_file = os.path.join(annotation_input, filename.replace('.jpg', '.xml'))
        annotation_content = convert_xml_to_coco_format(annotation_file)
        with open(os.path.join(train_output, 'labels', 'val',filename.replace('.jpg', '.txt')), 'w') as f:
            f.write(annotation_content)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--train-input", type=str, required=True)
    parser.add_argument("--annotation-input", type=str, required=True)
    parser.add_argument("--train-output", type=str, required=True)
    args = parser.parse_args()

    main(
        args.train_input,
        args.annotation_input,
        args.train_output,
    )