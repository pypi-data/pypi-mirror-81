#!/usr/bin/env python2

"""
    Dragon 32
    ~~~~~~~~~

    :created: 2014 by Jens Diemer - www.jensdiemer.de
    :copyleft: 2014 by the DragonPy team, see AUTHORS for more details.
    :license: GNU GPL v3 or above, see LICENSE for more details.
"""


import logging

from dragonpy.core.gui import DragonTkinterGUI
from dragonpy.core.machine import MachineGUI
from dragonpy.Dragon32.config import Dragon32Cfg
from dragonpy.Dragon32.periphery_dragon import Dragon32Periphery


log = logging.getLogger(__name__)


def run_Dragon32(cfg_dict):
    machine = MachineGUI(
        cfg=Dragon32Cfg(cfg_dict)
    )
    machine.run(
        PeripheryClass=Dragon32Periphery,
        GUI_Class=DragonTkinterGUI
    )


# ------------------------------------------------------------------------------
