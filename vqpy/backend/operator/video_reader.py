import cv2
from loguru import logger
from vqpy.backend.operator.base import Operator
from vqpy.backend.frame import Frame
import time


class VideoReader(Operator):
    def __init__(self, video_path: str):
        self._cap = cv2.VideoCapture(video_path)
        self.frame_id = -1
        self.metadata = self.get_metadata()
        self.read_video_time = 0

    def get_metadata(self):
        frame_width = self._cap.get(cv2.CAP_PROP_FRAME_WIDTH)  # float
        frame_height = self._cap.get(cv2.CAP_PROP_FRAME_HEIGHT)  # float
        fps = self._cap.get(cv2.CAP_PROP_FPS)
        n_frames = int(self._cap.get(cv2.CAP_PROP_FRAME_COUNT))

        logger.info(f"Metadata of video is width={frame_width}, \
                      height={frame_height}, fps={fps}, n_frames={n_frames}")
        metadata = dict(
            frame_width=frame_width,
            frame_height=frame_height,
            fps=fps,
            n_frames=n_frames,
        )
        return metadata

    def has_next(self) -> bool:
        if self.frame_id + 1 < self.metadata["n_frames"]:
            return True
        else:
            self.close()
            return False

    def next(self) -> Frame:
        if self.has_next():
            time_start = time.time()
            self.frame_id += 1
            ret_val, frame_image = self._cap.read()
            if not ret_val:
                logger.info(f"Failed to load frame stream with id of "
                            f"{self.frame_id}")
                raise IOError
            ch = cv2.waitKey(1)
            if ch == 27 or ch == ord("q") or ch == ord('Q'):
                raise KeyboardInterrupt

            frame = Frame(video_metadata=self.metadata,
                          id=self.frame_id,
                          image=frame_image)
            
            time_end = time.time()

            self.read_video_time += time_end - time_start
            with open('/home/chenyu97/Codes/vqpy/examples/aicity_query/result_check/read_video_time_cost', 'a') as file:
                file.write('read_video_time: ' + str(self.read_video_time) + '\n')

            return frame
        else:
            raise StopIteration

    def close(self):
        self._cap.release()
