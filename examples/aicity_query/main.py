import vqpy
from vqpy.frontend.vobj import VObjBase, vobj_property
from vqpy.frontend.query import QueryBase
from Codes.vqpy.examples.aicity_query.aicity_recognize import recognize
from Codes.vqpy.examples.aicity_query.aicity_recognize import prepare_recognize
from getcolor import get_color
import argparse
from vqpy.operator.detector import register as detector_register
from pathlib import Path
from Codes.vqpy.examples.aicity_query.fake_detector import FakeDetectorAicity
from vqpy.operator.tracker import register as tracker_register
from Codes.vqpy.examples.aicity_query.fake_tracker import FakeTrackerAicity
import time


'''
Query:
"02165c07-f8cf-42b5-84f9-6e7a73439b40": {
        "nl": [
            "red sedan go straight",
            "red sedan go straight",
            "red sedan go straight"
        ],
        "nl_other_views": []
    },

Track:
"a7f467cc-3f53-408d-b3cf-5d7fc221b4fd": {
    "frames": [
      "./train/S01/c004/img1/000478.jpg",
      "./train/S01/c004/img1/000479.jpg",
      "./train/S01/c004/img1/000480.jpg",
      "./train/S01/c004/img1/000481.jpg",
      "./train/S01/c004/img1/000482.jpg",
      "./train/S01/c004/img1/000483.jpg",
      "./train/S01/c004/img1/000484.jpg",
      "./train/S01/c004/img1/000485.jpg",
      "./train/S01/c004/img1/000486.jpg",
      "./train/S01/c004/img1/000487.jpg",
      "./train/S01/c004/img1/000488.jpg",
      "./train/S01/c004/img1/000489.jpg",
      "./train/S01/c004/img1/000490.jpg",
      "./train/S01/c004/img1/000491.jpg",
      "./train/S01/c004/img1/000492.jpg",
      "./train/S01/c004/img1/000493.jpg",
      "./train/S01/c004/img1/000494.jpg",
      "./train/S01/c004/img1/000495.jpg",
      "./train/S01/c004/img1/000496.jpg",
      "./train/S01/c004/img1/000497.jpg",
      "./train/S01/c004/img1/000498.jpg",
      "./train/S01/c004/img1/000499.jpg",
      "./train/S01/c004/img1/000500.jpg",
      "./train/S01/c004/img1/000501.jpg",
      "./train/S01/c004/img1/000502.jpg",
      "./train/S01/c004/img1/000503.jpg",
      "./train/S01/c004/img1/000504.jpg",
      "./train/S01/c004/img1/000505.jpg",
      "./train/S01/c004/img1/000506.jpg",
      "./train/S01/c004/img1/000507.jpg",
      "./train/S01/c004/img1/000508.jpg",
      "./train/S01/c004/img1/000509.jpg",
      "./train/S01/c004/img1/000510.jpg",
      "./train/S01/c004/img1/000511.jpg",
      "./train/S01/c004/img1/000512.jpg",
      "./train/S01/c004/img1/000513.jpg",
      "./train/S01/c004/img1/000514.jpg",
      "./train/S01/c004/img1/000515.jpg",
      "./train/S01/c004/img1/000516.jpg",
      "./train/S01/c004/img1/000517.jpg",
      "./train/S01/c004/img1/000518.jpg",
      "./train/S01/c004/img1/000519.jpg",
      "./train/S01/c004/img1/000520.jpg"
    ],
    "boxes": [
      [706, 213, 61, 51],
      [702, 216, 63, 52],
      [698, 218, 64, 53],
      [694, 221, 66, 54],
      [689, 223, 67, 55],
      [685, 226, 69, 56],
      [681, 228, 70, 58],
      [677, 231, 72, 59],
      [673, 233, 73, 60],
      [669, 236, 75, 61],
      [664, 238, 76, 62],
      [660, 241, 78, 63],
      [656, 243, 79, 64],
      [652, 243, 83, 68],
      [647, 249, 83, 72],
      [639, 250, 87, 77],
      [631, 255, 90, 77],
      [623, 260, 92, 77],
      [616, 265, 95, 78],
      [608, 270, 97, 78],
      [599, 272, 100, 81],
      [590, 276, 104, 88],
      [580, 280, 108, 95],
      [568, 289, 107, 94],
      [559, 297, 110, 95],
      [548, 303, 114, 95],
      [539, 314, 113, 96],
      [522, 321, 117, 103],
      [508, 329, 123, 107],
      [475, 345, 143, 110],
      [468, 351, 141, 121],
      [457, 362, 142, 117],
      [423, 380, 156, 131],
      [398, 395, 167, 143],
      [373, 409, 177, 155],
      [330, 444, 195, 147],
      [277, 459, 243, 194],
      [216, 479, 271, 205],
      [180, 519, 269, 217],
      [144, 558, 267, 228],
      [72, 606, 300, 263],
      [0, 654, 332, 298],
      [0, 714, 279, 346]
    ]
  }
  [x, y, x_len, y_len]
'''

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
        print(color)
        return color

    @vobj_property(inputs={"image": 0})
    def type(self, values):
        image = values["image"]
        reference = ["pickup-truck", "sedan", "suv", "van", "bus", "hatchback", "truck"]
        type = recognize(self.type_detect_transform, self.type_detect_model, image, reference)
        print(type)
        return type

    @vobj_property(inputs={"image": 0})
    def direction(self, values):
        image = values["image"]
        reference = [ "straight", "right", "left", "stop"]
        direction = recognize(self.direction_detect_transform, self.direction_detect_model, image, reference)
        print(direction)
        return direction


class ListRedSedanStraightCar(QueryBase):
    def __init__(self, object_detector_name, recognize_parameters):
        self.car = Car()
        self.car.set_object_detector(object_detector_name)
        self.car.set_color_recognize(recognize_parameters["color_model"], recognize_parameters["color_transform"])
        self.car.set_type_recognize(recognize_parameters["type_model"], recognize_parameters["type_transform"])
        self.car.set_direction_recognize(recognize_parameters["direction_model"], recognize_parameters["direction_transform"])

    def frame_constraint(self):
        return (self.car.score > 0.6) 
               #& (self.car.color.cmp(lambda color: "black" in color)) \
               #& (self.car.type.cmp(lambda type: "sedan" in type)) \
               #& (self.car.direction.cmp(lambda direction: "straight" in direction))

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
    #name_list = ["c026", "c027"]

    tracker_register("fake_tracker_aicity", FakeTrackerAicity)

    for name in name_list:
        print("Querying the video: " + name)

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
            output_per_frame_results=True,
        )

        vqpy.run(executor=query_executor, save_folder=args.save_folder, query_video_name=name)
    
    end_time = time.time()
    print("one query cost time: " + str(end_time - start_time))