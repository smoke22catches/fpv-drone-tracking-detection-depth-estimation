# Real time FPV drone detection, tracking and depth estimation

The purpose of this project is to develop a real-time FPV drone detection, tracking and depth estimation system in real time.

Todo:
- [ ] Prepare datasets
- [ ] Detection
- [ ] Tracking
- [ ] Depth estimation

Datasets:
- https://github.com/Maciullo/DroneDetectionDataset

## Dataset preparation

In order to train the model, we need to convert the dataset to YOLO format.

### Convert DroneDetectionDataset to YOLO format

```bash
python utils/convert_drone_detection_dataset_to_yolo_format.py --train-input datasets/Drone_TrainSet_100Snippet/ --annotation-input datasets/Drone_TrainSet_XMLs_100Snippet/ --train-output datasets/drone_detection_yolo
```