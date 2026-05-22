import cv2


class WebcamStream:

    def __init__(self, src=0):

        self.cap = cv2.VideoCapture(src)

        self.cap.set(
            cv2.CAP_PROP_FRAME_WIDTH,
            640
        )

        self.cap.set(
            cv2.CAP_PROP_FRAME_HEIGHT,
            480
        )

        if not self.cap.isOpened():

            raise RuntimeError(
                "Unable to open webcam"
            )

    def read(self):

        ret, frame = self.cap.read()

        if not ret:

            return None

        return frame

    def release(self):

        self.cap.release()