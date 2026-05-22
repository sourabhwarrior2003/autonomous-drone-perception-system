from ultralytics import YOLO


class YOLODetector:

    def __init__(self, model_path="yolov8n.pt"):

        self.model = YOLO(model_path)

    def detect(self, frame):

        results = self.model(
            frame,
            verbose=False
        )

        detections = []

        for result in results:

            boxes = result.boxes

            for box in boxes:

                x1, y1, x2, y2 = (
                    box.xyxy[0].tolist()
                )

                confidence = float(
                    box.conf[0]
                )

                class_id = int(
                    box.cls[0]
                )

                detections.append({

                    "bbox": [
                        int(x1),
                        int(y1),
                        int(x2),
                        int(y2)
                    ],

                    "confidence": confidence,

                    "class_id": class_id
                })

        return detections