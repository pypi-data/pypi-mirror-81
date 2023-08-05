#!/usr/bin/env python2

"""
    Dragon 32
    ~~~~~~~~~

    :created: 2014 by Jens Diemer - www.jensdiemer.de
    :copyleft: 2014 by the DragonPy team, see AUTHORS for more details.
    :license: GNU GPL v3 or above, see LICENSE for more details.
"""


import logging

from dragonpy.CoCo.config import CoCo2bCfg
from dragonpy.CoCo.periphery_coco import CoCoPeriphery
from dragonpy.core.gui import DragonTkinterGUI
from dragonpy.core.machine import MachineGUI


log = logging.getLogger(__name__)


def run_CoCo2b(cfg_dict):
    machine = MachineGUI(
        cfg=CoCo2bCfg(cfg_dict)
    )
    machine.run(
        PeripheryClass=CoCoPeriphery,
        GUI_Class=DragonTkinterGUI
    )
