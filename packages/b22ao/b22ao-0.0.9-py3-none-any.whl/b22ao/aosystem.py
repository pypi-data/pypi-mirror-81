from epics import caget, caput, camonitor
from b22ao.pvs import *
from enum import Enum
from threading import Event
import numpy


class AOSystem:

    def __init__(self):
        self.cam = AreaDetector(AD_PVBASE)
        self.dm = None  # DM of choice

    def select_dm(self, dm):
        self.dm = DeformableMirror(dm)

    def deform(self, mask, dm=None):
        try:
            DeformableMirror(dm).deform(mask)
        except ValueError:  # no dm provided
            try:
                self.dm.deform(mask)
            except AttributeError:
                raise NameError("Call #select_dm(dm) first or specify a DM in #deform(mask, dm)")

    def capture(self):
        return self.cam.acquire()

    def get_metadata(self):
        return {'cam': self.cam.get_metadata(), 'dm': self.dm.get_metadata()}


class DeformableMirror(Enum):

    DM1 = 1
    DM2 = 2

    def deform(self, mask):
        for actuator in range(len(mask)):
            caput(self._get_pv_base() + DM_ACTUATOR_PREFIX + str(actuator) + DM_ACTUATOR_SETPOINT, mask[actuator])
        caput(self._get_pv_base() + DM_APPLY_MASK, 1)

    def _get_pv_base(self):
        if self is DeformableMirror.DM1:
            return standardise_pv(DM1_PVBASE)
        elif self is DeformableMirror.DM2:
            return standardise_pv(DM2_PVBASE)

    def get_metadata(self):
        return {'mirror': self}


class AreaDetector:

    def __init__(self, pv_base):
        pv_base = standardise_pv(pv_base)
        self.data_ready = Event()
        self.current_frame = None
        self.frame_counter_pv = pv_base + AD_ARRAY_COUNTER
        self.acquire_pv = pv_base + AD_ACQUIRE
        self.data_pv = pv_base + AD_ARRAY_DATA
        self.dim_x_pv = pv_base + AD_DIM_X
        self.dim_y_pv = pv_base + AD_DIM_Y
        self.gain_pv = pv_base + AD_GAIN

        caput(pv_base + AD_IMAGE_MODE, AD_IMAGE_MODE_SINGLE)

        camonitor(self.frame_counter_pv, callback=self.frame_counter_callback)

    def acquire(self):
        self.current_frame = caget(self.frame_counter_pv)
        caput(self.acquire_pv, "Acquire")
        self.data_ready.wait()
        data = caget(self.data_pv)
        self.data_ready.clear()
        data = numpy.reshape(data, (caget(self.dim_y_pv), caget(self.dim_x_pv)))
        return data

    def frame_counter_callback(self, **kwargs):
        if kwargs['value'] == self.current_frame + 1:
            self.data_ready.set()

    def get_metadata(self):
        metadata = dict()
        metadata['gain'] = caget(self.gain_pv)
        return metadata


def standardise_pv(pv):
    return pv if pv.endswith(':') else pv + ':'
