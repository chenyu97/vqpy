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
from collections import Counter
import time
from optimal_order_with_history import obtain_optimal_order
import json


REUSE_TIMESCALE_THRESHOLD = 10


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
    
    @vobj_property(inputs={"image": 0, "color": REUSE_TIMESCALE_THRESHOLD})
    def color(self, values):
        #print("show color list: " + str(values['color']))
        counter = Counter(values["color"][:-1])
        most_common_element, count = counter.most_common(1)[0]
        if (most_common_element != None) and (count > (REUSE_TIMESCALE_THRESHOLD / 2.0)):
            return most_common_element
        else:
            image = values["image"]
            reference = ["blue", "green", "black", "white", "red", "grey", "silver", "brown"]
            color = recognize(self.color_detect_transform, self.color_detect_model, image, reference)
            return color

    @vobj_property(inputs={"image": 0, "type": REUSE_TIMESCALE_THRESHOLD})
    def type(self, values):
        #print("show type list: " + str(values['type']))
        counter = Counter(values["type"][:-1])
        most_common_element, count = counter.most_common(1)[0]
        if (most_common_element != None) and (count > (REUSE_TIMESCALE_THRESHOLD / 2.0)):
            return most_common_element
        else:
            image = values["image"]
            reference = ["pickup-truck", "sedan", "suv", "van", "bus", "hatchback", "truck"]
            type = recognize(self.type_detect_transform, self.type_detect_model, image, reference)
            return type

    @vobj_property(inputs={"image": 0})
    def direction(self, values):
        image = values["image"]
        reference = [ "straight", "right", "left", "stop"]
        direction = recognize(self.direction_detect_transform, self.direction_detect_model, image, reference)
        #print(direction)
        return direction


class MyQuery(QueryBase):
    def __init__(self, object_detector_name, recognize_parameters):
        self.car = Car()
        self.car.set_object_detector(object_detector_name)
        self.car.set_color_recognize(recognize_parameters["color_model"], recognize_parameters["color_transform"])
        self.car.set_type_recognize(recognize_parameters["type_model"], recognize_parameters["type_transform"])
        self.car.set_direction_recognize(recognize_parameters["direction_model"], recognize_parameters["direction_transform"])

    def frame_constraint(self):
        pass

    def frame_output(self):
        return (
            self.car.track_id,
            self.car.color,
            self.car.type,
            self.car.direction,
        )


class MyQueryOrder1(MyQuery):
    def __init__(self, query, object_detector_name, recognize_parameters):
        self.query = query
        super().__init__(object_detector_name, recognize_parameters)
    
    def frame_constraint(self):
        return (self.car.score > 0.6) \
                & (self.car.color == self.query['color']) \
                & (self.car.type == self.query['type']) \
                & (self.car.direction == self.query['direction'])


class MyQueryOrder2(MyQuery):
    def __init__(self, query, object_detector_name, recognize_parameters):
        self.query = query
        super().__init__(object_detector_name, recognize_parameters)
    
    def frame_constraint(self):
        return (self.car.score > 0.6) \
                & (self.car.color == self.query['color']) \
                & (self.car.direction == self.query['direction']) \
                & (self.car.type == self.query['type'])


class MyQueryOrder3(MyQuery):
    def __init__(self, query, object_detector_name, recognize_parameters):
        self.query = query
        super().__init__(object_detector_name, recognize_parameters)
    
    def frame_constraint(self):
        return (self.car.score > 0.6) \
                & (self.car.type == self.query['type']) \
                & (self.car.color == self.query['color']) \
                & (self.car.direction == self.query['direction'])
    

class MyQueryOrder4(MyQuery):
    def __init__(self, query, object_detector_name, recognize_parameters):
        self.query = query
        super().__init__(object_detector_name, recognize_parameters)
    
    def frame_constraint(self):
        return (self.car.score > 0.6) \
                & (self.car.type == self.query['type']) \
                & (self.car.direction == self.query['direction']) \
                & (self.car.color == self.query['color'])


class MyQueryOrder5(MyQuery):
    def __init__(self, query, object_detector_name, recognize_parameters):
        self.query = query
        super().__init__(object_detector_name, recognize_parameters)
    
    def frame_constraint(self):
        return (self.car.score > 0.6) \
                & (self.car.direction == self.query['direction']) \
                & (self.car.color == self.query['color']) \
                & (self.car.type == self.query['type'])


class MyQueryOrder6(MyQuery):
    def __init__(self, query, object_detector_name, recognize_parameters):
        self.query = query
        super().__init__(object_detector_name, recognize_parameters)
    
    def frame_constraint(self):
        return (self.car.score > 0.6) \
                & (self.car.direction == self.query['direction']) \
                & (self.car.type == self.query['type']) \
                & (self.car.color == self.query['color'])
     

if __name__ == "__main__":
    # input query
    query = {'color': 'black', 'type': 'sedan', 'direction': 'straight'}

    # read offline profile
    profile_path = './resources/offline_profile_1.json'
    profile_data = None
    with open(profile_path, 'r') as file:
        profile_data = json.load(file)

    # define dictionary of order and its query class
    order_query_dict = {
                    'color_type_direction':MyQueryOrder1, \
                    'color_direction_type':MyQueryOrder2, \
                    'type_color_direction':MyQueryOrder3, \
                    'type_direction_color':MyQueryOrder4, \
                    'direction_color_type':MyQueryOrder5, \
                    'direction_type_color':MyQueryOrder6
                    }

    start_time = time.time()

    # prepare models for color, type, direction
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

    # prepare video names
    video_name_list = []
    for index in range(1, 6):
        video_name_list.append("c00" + str(index))
    for index in range(10, 41):
        video_name_list.append("c0" + str(index))

    # register tracker
    tracker_register("fake_tracker_aicity", FakeTrackerAicity)

    # query on videos
    for video_name in video_name_list:
        print("Querying the video: " + video_name)

        # register object detector
        resource_dir = Path(Path(__file__).parent, "resources")
        precomputed_path = (resource_dir / (video_name + ".json")).as_posix()        
        detector_name = "fake_detector_aicity_" + video_name
        detector_register(detector_name, FakeDetectorAicity, precomputed_path, None)

        # parse arguments
        parser = argparse.ArgumentParser()
        parser.add_argument("--path", help="path to video file",
                            default="./input_videos/" + video_name + ".mp4")
        parser.add_argument("--save_folder", help="path to save query result",
                            default="./results_vqpy_annotation_optimal_order/" + query["color"] + '_' + query["type"] + '_' + query["direction"] + "/")
        args = parser.parse_args()

        # obtain optimal order
        opt_order = obtain_optimal_order(profile_data, video_name, query, REUSE_TIMESCALE_THRESHOLD)
        query_selected = order_query_dict[opt_order[0] + '_' + opt_order[1] + '_' + opt_order[2]]
        
        # initialize and run query
        query_executor = vqpy.init(
            video_path=args.path,
            query_obj=query_selected(query=query, object_detector_name=detector_name, recognize_parameters=recognize_par),
            verbose=True,
            output_per_frame_results=True,
        )
        vqpy.run(executor=query_executor, save_folder=args.save_folder, query_video_name=video_name)
    
    end_time = time.time()
    print('query_cost_time: ' + str(end_time - start_time))