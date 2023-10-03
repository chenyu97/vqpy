import vqpy
from vqpy.frontend.vobj import VObjBase, vobj_property
from vqpy.frontend.query import QueryBase
from aicity_recognize import recognize
from aicity_recognize import prepare_recognize
import argparse
from vqpy.operator.detector import register as detector_register
from pathlib import Path
from fake_detector import FakeDetectorAicity
from vqpy.operator.tracker import register as tracker_register
from fake_tracker import FakeTrackerAicity
import time


class Car(VObjBase):
    def __init__(self):
        self.class_name = "car"
        self.object_detector = ""
        self.detector_kwargs = {"device": "gpu"}
        self.object_tracker = "fake_tracker_aicity"
        
        self.color_detect_model = None
        self.color_detect_transform = None
        self.type_detect_model = None
        self.type_detect_transform = None
        self.direction_detect_model = None
        self.direction_detect_transform = None

        super().__init__()
    
    def set_object_detector(self, object_detector_name):
        self.object_detector = object_detector_name
    
    def set_color_recognize(self, color_detect_model, color_detect_transform):
        self.color_detect_model = color_detect_model
        self.color_detect_transform = color_detect_transform
    
    def set_type_recognize(self, type_detect_model, type_detect_transform):
        self.type_detect_model = type_detect_model
        self.type_detect_transform = type_detect_transform
    
    def set_direction_recognize(self, direction_detect_model, direction_detect_transform):
        self.direction_detect_model = direction_detect_model
        self.direction_detect_transform = direction_detect_transform
    
    @vobj_property(inputs={"image": 0})
    def color(self, values):
        image = values["image"]
        reference = ["blue", "green", "black", "white", "red", "grey", "silver", "brown"]
        color = recognize(self.color_detect_transform, self.color_detect_model, image, reference)
        #print(color)
        return color

    @vobj_property(inputs={"image": 0})
    def type(self, values):
        image = values["image"]
        reference = ["pickup-truck", "sedan", "suv", "van", "bus", "hatchback", "truck"]
        type = recognize(self.type_detect_transform, self.type_detect_model, image, reference)
        #print(type)
        return type

    @vobj_property(inputs={"image": 0})
    def direction(self, values):
        image = values["image"]
        reference = [ "straight", "right", "left", "stop"]
        direction = recognize(self.direction_detect_transform, self.direction_detect_model, image, reference)
        #print(direction)
        return direction


class ListRedSedanStraightCar(QueryBase):
    def __init__(self, object_detector_name, recognize_parameters):
        self.car = Car()
        self.car.set_object_detector(object_detector_name)
        self.car.set_color_recognize(recognize_parameters["color_model"], recognize_parameters["color_transform"])
        self.car.set_type_recognize(recognize_parameters["type_model"], recognize_parameters["type_transform"])
        self.car.set_direction_recognize(recognize_parameters["direction_model"], recognize_parameters["direction_transform"])

    def frame_constraint(self):
        return (self.car.score > 0.6) \
               & (self.car.color.cmp(lambda color: "black" in color)) \
               & (self.car.type.cmp(lambda type: "sedan" in type)) \
               & (self.car.direction.cmp(lambda direction: "straight" in direction))

    def frame_output(self):
        return (
            self.car.track_id,
            self.car.color,
            self.car.type,
            self.car.direction,
        )


if __name__ == "__main__":
    start_time = time.time()

    transform_color, model_color = prepare_recognize("color")
    transform_type, model_type = prepare_recognize("type")
    transform_direction, model_direction = prepare_recognize("direction")

    recognize_par = {}
    recognize_par["color_model"] = model_color
    recognize_par["color_transform"] = transform_color
    recognize_par["type_model"] = model_type
    recognize_par["type_transform"] = transform_type
    recognize_par["direction_model"] = model_direction
    recognize_par["direction_transform"] = transform_direction

    name_list = []
    for index in range(1, 6):
        name_list.append("c00" + str(index))
    for index in range(10, 41):
        name_list.append("c0" + str(index))

    tracker_register("fake_tracker_aicity", FakeTrackerAicity)

    for name in name_list:
        #print("Querying the video: " + name)
        resource_dir = Path(Path(__file__).parent, "resources")
        precomputed_path = (resource_dir / (name + ".json")).as_posix()
        
        detector_name = "fake_detector_aicity_" + name
        detector_register(detector_name, FakeDetectorAicity, precomputed_path, None)

        parser = argparse.ArgumentParser()
        parser.add_argument("--path", help="path to video file",
                            default="./input_videos/" + name + ".mp4")
        parser.add_argument("--save_folder", help="path to save query result")
        args = parser.parse_args()
        
        query_executor = vqpy.init(
            video_path=args.path,
            query_obj=ListRedSedanStraightCar(object_detector_name=detector_name, recognize_parameters=recognize_par),
            verbose=True,
            output_per_frame_results=False,
        )
        return_result = vqpy.run(executor=query_executor, save_folder=args.save_folder, print_results=False, query_video_name=name)
        
        for r in return_result:
            pass
        
    end_time = time.time()
    total_time_exc = end_time - start_time

    print('total_time_exc: ' + str(total_time_exc))