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
from collections import Counter
from getvelocity import get_velocity


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
    
    @vobj_property(inputs={"tlbr": 1})
    def velocity(self, values):
        last_tlbr, tlbr = values["tlbr"]
        velocity = get_velocity(last_tlbr, tlbr)
        return velocity
    

class MyQuery(QueryBase):
    def __init__(self, query, recognize_parameters):
        self.car = Car()
        self.query = query
        self.car.set_color_recognize(recognize_parameters["color_model"], recognize_parameters["color_transform"])

    def frame_constraint(self):
        return (self.car.velocity > 1) \
                & (self.car.color == self.query['color']) \

    def frame_output(self):
        return (
            self.car.track_id,
            self.car.tlbr
        )
     

if __name__ == "__main__":
    # input query
    query = {'color': 'red', 'type': 'suv', 'direction': 'right'}

    # prepare models for color, type, direction
    transform_color, model_color = prepare_recognize("color")
    recognize_par = {}
    recognize_par["color_model"] = model_color
    recognize_par["color_transform"] = transform_color

    # prepare video names
    name_list = ['../../../Three_Datasets/Banff/cut_videos/3min_banff_sat_am001.mp4',
                '../../../Three_Datasets/Banff/banff_sat_am001.mp4',
                '../../../Three_Datasets/Jackson/cut_videos/3min_jacksonhole_sat_am000.mp4',
                '../../../Three_Datasets/Jackson/jacksonhole_sat_am000.mp4',
                '../../../Three_Datasets/Southampton/cut_videos/3min_raw000.mp4',
                '../../../Three_Datasets/Southampton/raw000.mp4']

    # query on videos
    for index, name in enumerate(name_list):
        print("Querying the video: " + name)
        start_time = time.time()
        # parse arguments
        parser = argparse.ArgumentParser()
        parser.add_argument("--path", help="path to video file",
                            default=name)
        parser.add_argument("--save_folder", help="path to save query result",
                            default="./results_Q3/" + query["color"] + '_' + query["type"] + '_' + query["direction"] + "/")
        args = parser.parse_args()
        
        # initialize and run query
        query_executor = vqpy.init(
            video_path=args.path,
            query_obj=MyQuery(query=query, recognize_parameters=recognize_par),
            verbose=True,
            output_per_frame_results=True,
        )
        vqpy.run(executor=query_executor, save_folder=args.save_folder)
        end_time = time.time()
        with open('./result/Q3_time_cost_' + str(index) + '_' + str(time.time()), 'a') as file:
            file.write('query_cost_time: ' + str(end_time - start_time))