# Real time FPV drone detection and last mile guidance

The purpose of this project is to implement real time FPV drone software for detecting other drones and providing last mile guidance for them. The final product should be a software that could be deployed on drone board computer and which allow to automatically track drones and provide guidance to intercept them.

To achive this result the computer vision model would be trained and optimized for single board computer like Raspberry Pi or Jetson Orin Nano. Also the simulation will be implemented using Project AirSim.

The whole project should be automated using MLOps practices.

Todo:

[] Setup Project AirSim for drone detection simulation
[] Provide stream from Project AirSim camera to simulation script and output screenshots for demo
[] Run detection model on AirSim stream

Datasets:

- https://github.com/Maciullo/DroneDetectionDataset
