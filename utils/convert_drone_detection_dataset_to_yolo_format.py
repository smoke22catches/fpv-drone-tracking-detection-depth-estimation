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

def main(train_input: str, annotation_input: str, train_output: str, test_input: str, test_annotation_input: str) -> None:
    if not os.path.exists(train_output):
        os.makedirs(train_output)

    # Check if images and labels folders exist, then recreate folder structure
    images_path = os.path.join(train_output, 'images')
    labels_path = os.path.join(train_output, 'labels')

    if os.path.exists(images_path):
        shutil.rmtree(images_path)

    if os.path.exists(labels_path):
        shutil.rmtree(labels_path)
    
    os.makedirs(images_path)
    os.makedirs(labels_path)
    os.makedirs(os.path.join(images_path, 'train'))
    os.makedirs(os.path.join(images_path, 'val'))
    os.makedirs(os.path.join(images_path, 'test'))
    os.makedirs(os.path.join(labels_path, 'train'))
    os.makedirs(os.path.join(labels_path, 'val'))
    os.makedirs(os.path.join(labels_path, 'test'))

    # split train_files into train and val in 80/20 ratio
    train_files = os.listdir(train_input)
    train_files_len = len(train_files)
    train_files_train = train_files[:int(train_files_len * 0.8)]
    train_files_val = train_files[int(train_files_len * 0.8):]

    # Iterate over all files in train_input folder and copy them to train_output folder
    for filename in train_files_train:
        src_file = os.path.join(train_input, filename)
        dst_file = os.path.join(train_output, 'images', 'train', filename)
        annotation_file = os.path.join(annotation_input, filename.replace('.jpg', '.xml'))

        if not os.path.exists(src_file) or not os.path.exists(annotation_file):
            continue

        shutil.copy2(src_file, dst_file)
        annotation_content = convert_xml_to_coco_format(annotation_file)
        with open(os.path.join(train_output, 'labels', 'train', filename.replace('.jpg', '.txt')), 'w') as f:
            f.writelines(annotation_content)
            f.writelines('\n')

    for filename in train_files_val:
        src_file = os.path.join(train_input, filename)
        dst_file = os.path.join(train_output, 'images', 'val', filename)
        shutil.copy2(src_file, dst_file)
        annotation_file = os.path.join(annotation_input, filename.replace('.jpg', '.xml'))
        annotation_content = convert_xml_to_coco_format(annotation_file)
        with open(os.path.join(train_output, 'labels', 'val', filename.replace('.jpg', '.txt')), 'w') as f:
            f.writelines(annotation_content)
            f.writelines('\n')

    test_files = os.listdir(test_input)
    for filename in test_files:
        src_file = os.path.join(test_input, filename)
        dst_file = os.path.join(train_output, 'images', 'test', filename)
        annotation_file = os.path.join(test_annotation_input, filename.replace('.jpg', '.xml'))

        if not os.path.exists(src_file) or not os.path.exists(annotation_file):
            continue

        shutil.copy2(src_file, dst_file)
        annotation_content = convert_xml_to_coco_format(annotation_file)
        with open(os.path.join(train_output, 'labels', 'test', filename.replace('.jpg', '.txt')), 'w') as f:
            f.writelines(annotation_content)
            f.writelines('\n')

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--train-input", type=str, required=True)
    parser.add_argument("--annotation-input", type=str, required=True)
    parser.add_argument("--train-output", type=str, required=True)
    parser.add_argument("--test-input", type=str, required=False, default=None)
    parser.add_argument("--test-annotation-input", type=str, required=False, default=None)
    args = parser.parse_args()

    main(
        args.train_input,
        args.annotation_input,
        args.train_output,
        args.test_input,
        args.test_annotation_input,
    )