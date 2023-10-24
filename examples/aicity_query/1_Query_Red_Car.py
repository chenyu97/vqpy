import vqpy
from vqpy.frontend.vobj import VObjBase, vobj_property
from vqpy.frontend.query import QueryBase
from aicity_recognize import recognize
from aicity_recognize import prepare_recognize
import argparse
from pathlib import Path
import time
from collections import Counter


REUSE_TIMESCALE_THRESHOLD = 10


class Car(VObjBase):
    def __init__(self):
        self.class_name = "car"
        self.object_detector = "yolov8m"
        self.detector_kwargs = {"device": 0}
        self.object_tracker = "byte"
        #self.object_tracker = "norfair"
        
        self.color_detect_model = None
        self.color_detect_transform = None

        super().__init__()
    
    def set_color_recognize(self, color_detect_model, color_detect_transform):
        self.color_detect_model = color_detect_model
        self.color_detect_transform = color_detect_transform
    
    @vobj_property(inputs={"image": 0, "color": REUSE_TIMESCALE_THRESHOLD})
    def color(self, values):
        print("show color list: " + str(values['color']))
        counter = Counter(values["color"][:-1])
        most_common_element, count = counter.most_common(1)[0]
        if (most_common_element != None) and (count > (REUSE_TIMESCALE_THRESHOLD / 2.0)):
            return most_common_element
        else:
            image = values["image"]
            reference = ["blue", "green", "black", "white", "red", "grey", "silver", "brown"]
            color = recognize(self.color_detect_transform, self.color_detect_model, image, reference)
            return color


class MyQuery(QueryBase):
    def __init__(self, query, recognize_parameters):
        self.car = Car()
        self.query = query
        self.car.set_color_recognize(recognize_parameters["color_model"], recognize_parameters["color_transform"])

    def frame_constraint(self):
        return (self.car.color == self.query['color'])

    def frame_output(self):
        return (
            self.car.tlbr,
        )
     

if __name__ == "__main__":
    # input query
    query = {'color': 'red', 'type': 'suv', 'direction': 'right'}

    start_time = time.time()
    
    # prepare models for color, type, direction
    transform_color, model_color = prepare_recognize("color")
    recognize_par = {}
    recognize_par["color_model"] = model_color
    recognize_par["color_transform"] = transform_color
    
    end_time = time.time()
    load_model_time = end_time - start_time

    # prepare video names
    name_list = []
    for index in range(1, 6):
        name_list.append("c00" + str(index))
    for index in range(10, 41):
        name_list.append("c0" + str(index))
    name_list = ["ua_detrac"]

    start_time = time.time()
    # query on videos
    for name in name_list:
        print("Querying the video: " + name)

        # parse arguments
        parser = argparse.ArgumentParser()
        parser.add_argument("--path", help="path to video file",
                            default="./input_videos/" + name + ".mp4")
        parser.add_argument("--save_folder", help="path to save query result",
                            default="./results_Q1/" + query["color"] + '_' + query["type"] + '_' + query["direction"] + "/")
        args = parser.parse_args()
        
        # initialize and run query
        query_executor = vqpy.init(
            video_path=args.path,
            query_obj=MyQuery(query=query, recognize_parameters=recognize_par),
            verbose=True,
            output_per_frame_results=True,
        )
        vqpy.run(executor=query_executor, save_folder=args.save_folder, query_video_name=name)
    
    end_time = time.time()
    print('load_model_cost_time: ' + str(load_model_time))
    print('query_cost_time: ' + str(end_time - start_time))