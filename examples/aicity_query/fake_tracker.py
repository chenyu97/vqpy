from __future__ import annotations
from typing import Dict, List, Tuple
from vqpy.operator.tracker.base import GroundTrackerBase

class FakeTrackerAicity(GroundTrackerBase):
    
    input_fields = ["index", "tlbr", "score"]
    output_fields = ["index", "track_id"]

    def __init__(self, fps):
        pass

    def update(self,
               frame_id: int,
               data: List[Dict]) -> Tuple[List[Dict], List[Dict]]:
        tracked_list = []
        for d in data:
            tracked_object = dict()
            tracked_object['index'] = d['index']
            tracked_object['track_id'] = d['score']
            tracked_list.append(tracked_object)
        empty_dict = dict()
        lost_list = [empty_dict]
        return (tracked_list, lost_list)