"""
    DragonPy
    ========

    :created: 2014 by Jens Diemer - www.jensdiemer.de
    :copyleft: 2014 by the DragonPy team, see AUTHORS for more details.
    :license: GNU GPL v3 or above, see LICENSE for more details.
"""


import logging

from dragonpy.core.machine import MachineGUI
from dragonpy.vectrex.config import VectrexCfg
from dragonpy.vectrex.periphery import VectrexPeriphery
from dragonpy.vectrex.vectrex_gui import VectrexGUI


log = logging.getLogger(__name__)


def run_Vectrex(cfg_dict):
    machine = MachineGUI(
        cfg=VectrexCfg(cfg_dict)
    )
    machine.run(
        PeripheryClass=VectrexPeriphery,
        GUI_Class=VectrexGUI
    )


# ------------------------------------------------------------------------------
