import vqpy
from vqpy.frontend.vobj import VObjBase, vobj_property
from vqpy.frontend.query import QueryBase
import math
import argparse
from getvelocity import get_velocity


class Car(VObjBase):
    def __init__(self):
        self.class_name = "car"
        self.object_detector = "yolox"
        self.detector_kwargs = {"device": "cpu"}
        self.object_tracker = "byte"
        super().__init__()

    @vobj_property(inputs={"tlbr": 1})
    def velocity(self, values):
        last_tlbr, tlbr = values["tlbr"]
        velocity = get_velocity(last_tlbr, tlbr)
        return velocity

class QuerySpeedingCar(QueryBase):
    def __init__(self):
        self.car = Car()

    def frame_constraint(self):
        return (self.car.score > 0.6) \
               & (self.car.velocity > 0.1)

    def frame_output(self):
        return (self.car.track_id, self.car.tlbr,)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", help="path to video file",
                        default="./license-10s.mp4")
    parser.add_argument("--save_folder", help="path to save query result",
                        default="./results/")
    args = parser.parse_args()
    query_executor = vqpy.init(
        video_path=args.path,
        query_obj=QuerySpeedingCar(),
        verbose=True,
    )
    vqpy.run(executor=query_executor, save_folder=args.save_folder)
