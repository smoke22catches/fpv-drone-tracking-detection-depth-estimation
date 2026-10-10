import argparse
import shutil
import os
import gdown
from utils.convert_drone_detection_dataset_to_yolo_format import convert_drone_detection_dataset_to_coco

SNIPPET_TRAIN = 'https://drive.google.com/file/d/1rRr821XZ6qvedc1x2ZFeZivEzESLLAOm/view?usp=sharing'
SNIPPET_TEST = 'https://drive.google.com/file/d/1gw08wFoN8Aop6BQBbYuCPGHiI8vQmTgI/view?usp=sharing'
FULL_TRAIN = 'https://drive.google.com/file/d/1lGumpFGdAvLWXhdLJCbkpv-Uo-t8fpHT/view?usp=sharing'
FULL_TEST = 'https://drive.google.com/file/d/1dJdUIqTfW7InN76Xb3flWVrVmcficP93/view?usp=sharing'

def main():
    # setup CLI parameters
    parser = argparse.ArgumentParser(prog='Download dataset')
    parser.add_argument('-s', '--snippet', action='store_true')
    args = parser.parse_args()

    # download dataset archives
    train_dataset_input = SNIPPET_TRAIN if args.snippet else FULL_TRAIN
    test_dataset_input = SNIPPET_TEST if args.snippet else FULL_TEST
    train_dataset_input_archive_path = "datasets/drone_detection_train.zip"
    test_dataset_input_archive_path = "datasets/drone_detection_test.zip"
    gdown.download(url=train_dataset_input, output=train_dataset_input_archive_path)
    gdown.download(url=test_dataset_input, output=test_dataset_input_archive_path)

    # unpack archives
    train_dataset_path = "datasets/drone_detection_train"
    shutil.unpack_archive(train_dataset_input_archive_path, train_dataset_path, "zip")
    test_dataset_path = "datasets/drone_detection_test"
    shutil.unpack_archive(test_dataset_input_archive_path, test_dataset_path, "zip")

    # convert dataset
    train_dataset_images = os.path.join(train_dataset_path, "Drone_TrainSet_100Snippet" if args.snippet else "Drone_TrainSet")
    train_dataset_annotations = os.path.join(train_dataset_path, "Drone_TrainSet_XMLs_100Snippet" if args.snippet else "Drone_TrainSet_XMLs")
    test_dataset_images = os.path.join(test_dataset_path, "Drone_TestSet_100Snippet" if args.snippet else "Drone_TestSet")
    test_dataset_annotations = os.path.join(test_dataset_path, "Drone_TestSet_XMLs_100Snippet" if args.snippet else "Drone_TestSet_XMLs")
    convert_drone_detection_dataset_to_coco(
        train_images_input=train_dataset_images,
        train_annotation_input=train_dataset_annotations,
        test_images_input=test_dataset_images,
        test_annotation_input=test_dataset_annotations,
        coco_format_output="datasets/drone_detection_yolo"
    )

if __name__ == '__main__':
    main()