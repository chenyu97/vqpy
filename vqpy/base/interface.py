"""Interfaces that requires implementations in impl/"""

from typing import Dict, List, Optional

from ..utils.video import FrameStream


class VObjBaseInterface(object):
    """The interface of VObject Base Class.
    The tracker is responsible to keep objects updated when the track is active
    """

    def __init__(self, ctx: FrameStream):
        self._ctx = ctx
        self._start_idx = ctx.frame_id
        # Number of frames consecutively appears
        self._track_length = 0
        # Historic object data. TODO: shrink memory
        self._datas: List[Optional[Dict]] = []
        # List of @property instances
        self._registered_names: List[str] = []
        raise NotImplementedError

    def getv(self,
             attr: str,
             index: int = -1,
             specifications: Optional[Dict[str, str]] = None):
        """
        attr: attribute name.
        index: FRAMEID - Current FRAMEID - 1.
        specifications: optional dictionary for specifying models.
        Return: the value when applicable, and None otherwise.
        """
        raise NotImplementedError

    def update(self, data: Optional[Dict]):
        """Called once per frame by the tracker providing the object data"""
        if data is not None:
            self._datas.append(data.copy())
            self._track_length += 1
        else:
            self._datas.append(None)
            self._track_length = 0
        raise NotImplementedError

    def infer(self,
              attr: str,
              specifications: Optional[Dict[str, str]] = None):
        """A easy-to-use interface provided for usage of built-in functions"""
        raise NotImplementedError
