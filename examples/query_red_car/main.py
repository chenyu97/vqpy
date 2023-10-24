import vqpy
from vqpy.frontend.vobj import VObjBase, vobj_property
from vqpy.frontend.query import QueryBase
import math
import argparse
from getcolor import get_color


class Car(VObjBase):
    def __init__(self):
        self.class_name = "car"
        self.object_detector = "yolox"
        self.detector_kwargs = {"device": "cpu"}
        self.object_tracker = "byte"
        super().__init__()

    @vobj_property(inputs={"image": 0})
    def color(self, values):
        image = values["image"]
        color = get_color(image)
        return color

class QueryRedCar(QueryBase):
    def __init__(self):
        self.car = Car()

    def frame_constraint(self):
        return (self.car.score > 0.6) \
               & (self.car.color == 'red')

    def frame_output(self):
        return (self.car.tlbr,)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", help="path to video file",
                        default="./license-10s.mp4")
    parser.add_argument("--save_folder", help="path to save query result",
                        default="./results/")
    args = parser.parse_args()
    query_executor = vqpy.init(
        video_path=args.path,
        query_obj=QueryRedCar(),
        verbose=True,
    )
    vqpy.run(executor=query_executor, save_folder=args.save_folder)
