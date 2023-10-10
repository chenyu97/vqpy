import json
from collections import deque, Counter


def video_to_tracks(video_name):
    file_path = './resources/test-tracks.json'
    data = None
    with open(file_path, 'r') as file:
        data = json.load(file)
    tracks_list = []
    for key, value in data.items():
        frames = value['frames']
        # only care tracks for video_name
        if frames[0][12:16] != video_name:
            continue
        cur_track = []
        last_frame_path = frames[0]
        for i in range(1, len(frames)):
            cur_track.append(key[:8] + '_F' + last_frame_path[-10:-4])
            gap = int(frames[i][-10:-4]) - int(last_frame_path[-10:-4])
            if gap != 1:
                # add None for non-continue tracks
                for no_continue_num in range(gap - 1):
                    cur_track.append(None)
            last_frame_path = frames[i]
        cur_track.append(key[:8] + '_F' + last_frame_path[-10:-4])
        tracks_list.append(cur_track)
    return tracks_list


def is_history_deque_enough_to_vote(history_deque, history_len):
    counter = Counter(history_deque)
    most_common_element, count = counter.most_common(1)[0]
    if (most_common_element != None) and (count > (history_len / 2.0)):
        return True, most_common_element    
    return False, None


def obtain_optimal_order(data, video_name, query, history_len):
    tracks_list = video_to_tracks(video_name)
    buffer_keys = ['color', 'type']
    options = ['color', 'type', 'direction']
    order_1_opt, order_2_opt, order_3_opt = None, None, None
    time_cost_min = float('inf')
    # for each possible order (order_1, order_2, order_3)
    for order_1 in options:
        for order_2 in options:
            if order_2 == order_1:
                continue
            for order_3 in options:
                if order_3 == order_1 or order_3 == order_2:
                    continue
                time_cost = 0
                # for each track, accumulate the time cost
                for track in tracks_list:
                    buffer_dict = dict()
                    for buffer_key in buffer_keys:
                        buffer_dict[buffer_key] = deque() 
                        for padding_num in range(history_len):
                            buffer_dict[buffer_key].append(None)
                    for profile_id in track:

                        if profile_id == None:
                            # for the element of None in non-continue tracks
                            for buffer_key in buffer_keys:
                                buffer_dict[buffer_key].append(None)
                                buffer_dict[buffer_key].popleft()
                        else:
                            profile_data = data[profile_id]

                            def get_result_and_cost(order_x, cost):
                                order_x_result = None
                                if order_x in buffer_keys: 
                                    is_enough, element = is_history_deque_enough_to_vote(buffer_dict[order_x], history_len)
                                    if is_enough:
                                        order_x_result = element
                                        cost += 0
                                    else:
                                        order_x_result = profile_data[order_x + '_result']
                                        cost += profile_data[order_x + '_cost']
                                    buffer_dict[order_x].append(order_x_result)
                                    buffer_dict[order_x].popleft()
                                else:
                                    order_x_result = profile_data[order_x + '_result']
                                    cost += profile_data[order_x + '_cost']
                                return order_x_result, cost

                            # get order_1_result
                            order_1_result, time_cost = get_result_and_cost(order_1, time_cost)
                            if order_1_result != query[order_1]:
                                if order_2 in buffer_keys:
                                    buffer_dict[order_2].append(None)
                                    buffer_dict[order_2].popleft()
                                if order_3 in buffer_keys:
                                    buffer_dict[order_3].append(None)
                                    buffer_dict[order_3].popleft()
                            else:
                                # get order_2_result
                                order_2_result, time_cost = get_result_and_cost(order_2, time_cost)
                                if order_2_result != query[order_2]:
                                    if order_3 in buffer_keys:
                                        buffer_dict[order_3].append(None)
                                        buffer_dict[order_3].popleft()
                                else:
                                    # get order_3_result
                                    order_3_result, time_cost = get_result_and_cost(order_3, time_cost)
                if time_cost < time_cost_min:
                    time_cost_min = time_cost
                    order_1_opt, order_2_opt, order_3_opt = order_1, order_2, order_3
    return (order_1_opt, order_2_opt, order_3_opt)


if __name__ == '__main__':
    file_path = './resources/offline_profile_1.json'
    data = None
    with open(file_path, 'r') as file:
        data = json.load(file)
    
    name_list = []
    for index in range(1, 6):
        name_list.append("c00" + str(index))
    for index in range(10, 41):
        name_list.append("c0" + str(index))

    for query_video in name_list:
        query = dict()
        query['color'] = 'black'
        query['type'] = 'sedan'
        query['direction'] = 'right'
        history_len = 10
        order_tuple = obtain_optimal_order(data, query_video, query, history_len)
        print(order_tuple)