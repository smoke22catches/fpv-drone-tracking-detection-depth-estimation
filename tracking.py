from collections import defaultdict
import argparse

import cv2
import numpy as np
import matplotlib.pyplot as plt

from ultralytics import YOLO

def main(model: str, video_path: str):
    model = YOLO(model)
    cap = cv2.VideoCapture(video_path)
    track_history = defaultdict(lambda: [])

    while cap.isOpened():
        success, frame = cap.read()
        if success:
            results = model.track(frame, persist=True)
            
            # Check if there are any detections
            if results[0].boxes is not None and len(results[0].boxes) > 0:
                boxes = results[0].boxes.xywh.cpu()
                annotated_frame = results[0].plot()
                
                # Check if tracking IDs exist
                if results[0].boxes.id is not None:
                    track_ids = results[0].boxes.id.int().cpu().tolist()
                    for box, track_id in zip(boxes, track_ids):
                        x, y, w, h = box
                        track = track_history[track_id]
                        track.append((float(x), float(y)))
                        if len(track) > 30:
                            track.pop(0)
                        points = np.hstack(track).astype(np.int32).reshape((-1, 1, 2))
                        cv2.polylines(annotated_frame, [points], isClosed=False, color=(230, 230, 230), thickness=10)
                else:
                    # No tracking IDs available, just show detections without trails
                    annotated_frame = results[0].plot()
            else:
                # No detections in this frame, create annotated frame anyway
                annotated_frame = frame
            
            cv2.imshow('outputs/tracking/track.jpg', annotated_frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        else:
            break
    
    cap.release()
    # ani = animation.ArtistAnimation(fig, frames)
    plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", type=str, required=True)
    parser.add_argument("--video-path", type=str, required=True)
    args = parser.parse_args()

    main(args.model, args.video_path)