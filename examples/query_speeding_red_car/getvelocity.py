import math


def get_velocity(last_tlbr, tlbr):
    fps = 25.0
    if last_tlbr is None or tlbr is None:
        return 0
    last_center = (last_tlbr[:2] + last_tlbr[2:]) / 2
    cur_center = (tlbr[:2] + tlbr[2:]) / 2
    tlbr_avg = (tlbr + last_tlbr) / 2
    scale = (tlbr_avg[3] - tlbr_avg[1]) / 1.5
    dcenter = (cur_center - last_center) / scale * fps
    return math.sqrt(sum(dcenter * dcenter))