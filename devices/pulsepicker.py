#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Module to define the PulsePicker device subclass.
"""
from copy import copy
from ophyd import EpicsSignalRO
from .lclscomponent import (LCLSComponent as Component,
                            LCLSFormattedComponent as FormattedComponent)
from .lclsdevice import LCLSDevice as Device
from .iocadmin import IOCAdminOld
from .state import (InOutStates, InOutCCMStates,
                    pvstate_class, statesrecord_class)


class PulsePicker(Device):
    """
    Device that lets us pick which beam pulses reach the sample.
    """
    in_out = FormattedComponent(InOutStates, "{self._in_out}",
                                ioc="{self._in_out_ioc}")
    blade = Component(EpicsSignalRO, ":READ_DF", string=True)
    mode = Component(EpicsSignalRO, ":SE", string=True)
    ioc = copy(Device.ioc)
    ioc.cls = IOCAdminOld

    def __init__(self, prefix, *, in_out="", ioc="", in_out_ioc="",
                 read_attrs=None, name=None, **kwargs):
        self._in_out = in_out
        self._in_out_ioc = in_out_ioc
        if read_attrs is None:
            read_attrs = ["mode", "blade", "in_out"]
        super().__init__(prefix, ioc=ioc, read_attrs=read_attrs, name=name,
                         **kwargs)

    def move_out(self):
        self.in_out.value = "OUT"

    def move_in(self):
        self.in_out.value = "IN"


class PulsePickerCCM(PulsePicker):
    """
    Device that lets us pick which beam pulses reach the sample.
    This is the version with a third position state in addition to IN and OUT,
    and that's the CCM state: IN but at the CCM offset.
    """
    in_out = copy(PulsePicker.in_out)
    in_out.cls = InOutCCMStates

    def move_ccm(self):
        self.in_out.value = "CCM"


TempStates = statesrecord_class("TempStates", ":PINK", ":CCM", ":OUT")
class PulsePickerPink(PulsePickerCCM):
    """
    Current state syntax that I plan to change
    """
    in_out = copy(PulsePickerCCM.in_out)
    in_out.cls = TempStates

    def move_in(self):
        self.in_out.value = "PINK"
