import cv2
import os

from src.camera.webcam_stream import WebcamStream
from src.detection.yolo_detector import YOLODetector
from src.utils.visualizer import draw_detections
from src.utils.fps import FPSCounter
from src.utils.logger import ProjectLogger


def main():

    # =========================
    # CREATE OUTPUT DIRECTORIES
    # =========================

    os.makedirs("outputs/screenshots", exist_ok=True)
    os.makedirs("outputs/videos", exist_ok=True)

    # =========================
    # LOGGER
    # =========================

    logger = ProjectLogger()

    logger.info("System initialized")

    # =========================
    # CAMERA
    # =========================

    stream = WebcamStream()

    logger.info("Webcam stream initialized")

    # =========================
    # DETECTOR
    # =========================

    detector = YOLODetector()

    logger.info("YOLO model loaded")

    # =========================
    # FPS COUNTER
    # =========================

    fps_counter = FPSCounter()

    # =========================
    # VIDEO WRITER
    # =========================

    fourcc = cv2.VideoWriter_fourcc(*'XVID')

    video_writer = cv2.VideoWriter(
        "outputs/videos/output.avi",
        fourcc,
        20.0,
        (640, 480)
    )

    logger.info("Video writer initialized")

    frame_count = 0

    # =========================
    # MAIN LOOP
    # =========================

    while True:

        frame = stream.read()

        if frame is None:

            logger.error("Failed to capture frame")

            break

        # =========================
        # DETECTION
        # =========================

        detections = detector.detect(frame)

        logger.info(f"Detections: {len(detections)}")

        # =========================
        # DRAW DETECTIONS
        # =========================

        frame = draw_detections(frame, detections)

        # =========================
        # FPS
        # =========================

        fps = fps_counter.update()

        logger.info(f"FPS: {fps}")

        cv2.putText(
            frame,
            f"FPS: {fps}",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 0, 255),
            2
        )

        # =========================
        # SAVE SCREENSHOT
        # =========================

        if frame_count % 100 == 0:

            screenshot_path = (
                f"outputs/screenshots/frame_{frame_count}.jpg"
            )

            cv2.imwrite(
                screenshot_path,
                frame
            )

            logger.info(
                f"Screenshot saved: {screenshot_path}"
            )

        # =========================
        # SAVE VIDEO
        # =========================

        video_writer.write(frame)

        # =========================
        # SHOW FRAME
        # =========================

        cv2.imshow(
            "Autonomous Drone Perception",
            frame
        )

        frame_count += 1

        key = cv2.waitKey(1)

        if key == ord('q'):

            logger.info("Exit key pressed")

            break

    # =========================
    # CLEANUP
    # =========================

    stream.release()

    video_writer.release()

    cv2.destroyAllWindows()

    logger.info("System shutdown")


if __name__ == "__main__":

    main()