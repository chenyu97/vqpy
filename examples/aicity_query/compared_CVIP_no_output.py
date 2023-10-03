import cv2
import json
from pathlib import Path
import time
from aicity_recognize import prepare_recognize
from aicity_recognize import recognize_id
from collections import Counter


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
    
    total_time_img = 0
    total_time_exc = 0
    total_time_infer = 0
    total_time_load_model = 0
    start_time_exc = time.time()
    
    start_time_load_model = time.time()
    transform_color, model_color = prepare_recognize("color")
    transform_type, model_type = prepare_recognize("type")
    transform_direction, model_direction = prepare_recognize("direction")
    end_time_load_model = time.time()
    total_time_load_model = end_time_load_model - start_time_load_model

    resource_dir = Path(Path(__file__).parent, "resources")
    file_path = (resource_dir / "test-tracks.json").as_posix()

    infer_result_color = {}
    infer_result_type = {}
    infer_result_direction = {}

    tracks_list = []
    
    with open(file_path, 'r') as file:
        data = json.load(file)
        tracks_list = list(data.keys())
        print_count = 0
        for key, value in data.items():
            if 'c001' not in value["frames"][0]:
                continue
            print_count += 1
            #print("detecting track_id: " + str(key) + "(" + str(print_count) + "/" + str(len(tracks_list)) + ")")
            color_result_list = []
            type_result_list = []
            direction_result_list = [] 
              
            for i in range(len(value["frames"])):
                bg_img_pth = value["frames"][i]
                bounding_box = value["boxes"][i]
                image_path = "./data/" + bg_img_pth
                
                start_time_img = time.time()
                image = cv2.imread(image_path)
                end_time_img = time.time()

                total_time_img += end_time_img - start_time_img
                
                if image is None:
                    raise ValueError("Fail to read image!")

                [x, y, w, h] = bounding_box
                cropped_image = image[y:y+h, x:x+w]

                start_time_infer = time.time()
                reference = ["blue", "green", "black", "white", "red", "grey", "silver", "brown"]
                color = recognize_id(transform_color, model_color, cropped_image, reference)
                color_result_list.append(color)

                reference = ["pickup-truck", "sedan", "suv", "van", "bus", "hatchback", "truck"]
                type = recognize_id(transform_type, model_type, cropped_image, reference)
                type_result_list.append(type)
        
                reference = [ "straight", "right", "left", "stop"]
                direction = recognize_id(transform_direction, model_direction, cropped_image, reference)
                direction_result_list.append(direction)
                end_time_infer = time.time()

                total_time_infer += end_time_infer - start_time_infer

            most_common_color = Counter(color_result_list).most_common(1)[0][0]
            most_common_type = Counter(type_result_list).most_common(1)[0][0]
            most_common_direction = Counter(direction_result_list).most_common(1)[0][0]
            
            infer_result_color[key] = dict()
            infer_result_color[key]["id"] = most_common_color

            infer_result_type[key] = dict()
            infer_result_type[key]["id"] = most_common_type

            infer_result_direction[key] = dict()
            infer_result_direction[key]["id"] = most_common_direction 

    end_time_exc = time.time()
    total_time_exc = end_time_exc - start_time_exc - total_time_img
    print("total_time_img: " + str(total_time_img) + ", total_time_infer: " + str(total_time_infer) + \
           ', total_time_exc: ' + str(total_time_exc) + ', total_time_load_model: ' + str(total_time_load_model))

'''
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
        if key != "04fd33a1-0228-408c-b146-fc0a1cd6b2a8":
                continue
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

    print("load_image_time: " + str(total_time)) 
'''
    #json.dump(final_rank, open('./results_compared_CVIP/result.json', 'w'), indent=4)

    