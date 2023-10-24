import vqpy
from vqpy.frontend.vobj import VObjBase, vobj_property
from vqpy.frontend.query import QueryBase
from aicity_recognize import recognize
from aicity_recognize import prepare_recognize
import argparse
from pathlib import Path
import time
from getvelocity import get_velocity


class Car(VObjBase):
    def __init__(self):
        self.class_name = "car"
        self.object_detector = "yolov8m"
        self.detector_kwargs = {"device": 0}
        self.object_tracker = "byte"
        #self.object_tracker = "norfair"

        super().__init__()

    @vobj_property(inputs={"tlbr": 1})
    def velocity(self, values):
        last_tlbr, tlbr = values["tlbr"]
        velocity = get_velocity(last_tlbr, tlbr)
        return velocity
    

class MyQuery(QueryBase):
    def __init__(self, query):
        self.car = Car()
        self.query = query

    def frame_constraint(self):
        return (self.car.velocity > 1)

    def frame_output(self):
        return (
            self.car.track_id,
            self.car.tlbr
        )
     

if __name__ == "__main__":
    # input query
    query = {'color': 'red', 'type': 'suv', 'direction': 'right'}

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
                            default="./results_Q2/" + query["color"] + '_' + query["type"] + '_' + query["direction"] + "/")
        args = parser.parse_args()
        
        # initialize and run query
        query_executor = vqpy.init(
            video_path=args.path,
            query_obj=MyQuery(query=query),
            verbose=True,
            output_per_frame_results=True,
        )
        vqpy.run(executor=query_executor, save_folder=args.save_folder)
        end_time = time.time()
        with open('./result/Q2_time_cost_' + str(index) + '_' + str(time.time()), 'a') as file:
            file.write('query_cost_time: ' + str(end_time - start_time))