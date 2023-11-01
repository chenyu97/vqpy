import cv2
import json
from pathlib import Path
import time
from aicity_recognize import prepare_recognize
from aicity_recognize import recognize_id
from collections import Counter
from vqpy.utils.images import crop_image
import numpy as np


def is_same(attr_text, attr_track):
    for attr in attr_track:
        if attr_track[attr] != attr_text[attr]:
            return False
    return True

def get_attr(u, colors_dict, types_dict, directions_dict):

    color = colors_dict[u]["id"]
    type = types_dict[u]["id"]
    direction = directions_dict[u]["id"]
    attr_track = {"colors": color, "type": type}

    return attr_track, direction


if __name__ == "__main__":

    transform_color, model_color = prepare_recognize("color")
    transform_type, model_type = prepare_recognize("type")
    transform_direction, model_direction = prepare_recognize("direction")

    resource_dir = Path(Path(__file__).parent, "resources")
    file_path = (resource_dir / "c005.json").as_posix()

    infer_result_color = {}
    infer_result_type = {}
    infer_result_direction = {}

    # create list of time cost for each frame in video c005
    frame_time_cost = [0] * 2110
    for f in range(len(frame_time_cost)):
        # time_for read image
        time_start= time.time()
        image_path = "./data/train/S01/c005/img1/" + "{:06}".format(f + 1) + ".jpg"
        image = cv2.imread(image_path)
        time_end = time.time()
        frame_time_cost[f] += time_end - time_start

    tracks_list = []

    with open(file_path, 'r') as file:
        data = json.load(file)
        tracks_list = list(data.keys())
        print_count = 0
        for key, value in data.items():
            print_count += 1
            print("detecting track_id: " + str(key) + "(" + str(print_count) + "/" + str(len(tracks_list)) + ")")
            color_result_list = []
            type_result_list = []
            direction_result_list = []    
            for i in range(len(value["frames"])):
                bg_img_pth = value["frames"][i]
                
                frame_id = int(bg_img_pth[-10:-4]) - 1

                bounding_box = value["boxes"][i]
                image_path = "./data/" + bg_img_pth
                image = cv2.imread(image_path)

                time_start = time.time()

                if image is None:
                    raise ValueError("Fail to read image!")

                [x, y, w, h] = bounding_box
                tlbr = [x, y, x+w, y+h]
                cropped_image = crop_image(image, np.array(tlbr, dtype=np.float64))

                reference = ["blue", "green", "black", "white", "red", "grey", "silver", "brown"]
                color = recognize_id(transform_color, model_color, cropped_image, reference)
                color_result_list.append(color)

                reference = ["pickup-truck", "sedan", "suv", "van", "bus", "hatchback", "truck"]
                type = recognize_id(transform_type, model_type, cropped_image, reference)
                type_result_list.append(type)
        
                reference = [ "straight", "right", "left", "stop"]
                direction = recognize_id(transform_direction, model_direction, cropped_image, reference)
                direction_result_list.append(direction) 

                time_end = time.time()

                frame_time_cost[frame_id] += time_end - time_start    

            most_common_color = Counter(color_result_list).most_common(1)[0][0]
            most_common_type = Counter(type_result_list).most_common(1)[0][0]
            most_common_direction = Counter(direction_result_list).most_common(1)[0][0]
            
            infer_result_color[key] = dict()
            infer_result_color[key]["id"] = most_common_color

            infer_result_type[key] = dict()
            infer_result_type[key]["id"] = most_common_type

            infer_result_direction[key] = dict()
            infer_result_direction[key]["id"] = most_common_direction

    colors_dict = infer_result_color 
    types_dict = infer_result_type
    directions_dict = infer_result_direction

    final_rank = {}

    reference_color = ["blue", "green", "black", "white", "red", "grey", "silver", "brown"]
    reference_type = ["pickup-truck", "sedan", "suv", "van", "bus", "hatchback", "truck"]
    reference_direction = [ "straight", "right", "left", "stop"]

    potential_cand = []
    potential2_cand = []
    unpotential_cand = []

    text_attr, text_direction = {"colors": 2, "type": 1}, {0}
    for track in tracks_list:
        track_attr, track_direction = get_attr(
            track, colors_dict, types_dict, directions_dict
        )
        ids = str(colors_dict[track]["id"]) + str(types_dict[track]["id"]) + str(directions_dict[track]["id"])
        if not is_same(text_attr, track_attr):
            unpotential_cand.append({track: ids})
        else:
            if track_direction == text_direction:
                potential_cand.append({track: ids})
            else:
                potential2_cand.append({track: ids})

    potential_cand = potential_cand + potential2_cand
    final_rank['track_id'] = potential_cand + unpotential_cand

    json.dump(final_rank, open('./results_compared_CVIP/result.json', 'w'), indent=4)

    with open("./results_compared_CVIP/drill_down_compared_CVIP", "a") as file:
        for index in range(len(frame_time_cost)):
            file.write(str(index) + ": " + str(frame_time_cost[index]) + "\n")
