# Real time FPV drone detection and last mile guidance

The purpose of this project is to implement real time FPV drone software for detecting other drones and providing last mile guidance for them. The final product should be a software that could be deployed on drone board computer and which allow to automatically track drones and provide guidance to intercept them.

To achive this result the computer vision model would be trained and optimized for single board computer like Raspberry Pi or Jetson Orin Nano. Also the simulation will be implemented using Project AirSim.

The whole project should be automated using MLOps practices.

Todo:

Training pipeline (MLOps)

- [x] Make separate script for downloading and splitting datasets
- [ ] Turn training pipeline from notebook into separate script
- [ ] Track training and save model using MLflow
- [ ] Automate creating instance on vast.ai and run training pipeline on it

Simulation (AirSim integration)

- [ ] Setup Project AirSim for drone detection simulation
- [ ] Provide stream from Project AirSim camera to simulation script and output screenshots for demo
- [ ] Run detection model on AirSim stream

Datasets:

- https://github.com/Maciullo/DroneDetectionDataset

# Project Setup

## 1. Download dataset

```
python dataset.py [-s]
```

Use `-s` or `--snippet` option only if snippet dataset is required. To download full dataset don't use it.
