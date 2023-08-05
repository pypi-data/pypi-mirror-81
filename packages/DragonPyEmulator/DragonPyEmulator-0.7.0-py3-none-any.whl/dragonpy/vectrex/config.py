"""
    DragonPy - Vectrex
    ==================

    https://en.wikipedia.org/wiki/Vectrex

    :created: 2014 by Jens Diemer - www.jensdiemer.de
    :copyleft: 2014 by the DragonPy team, see AUTHORS for more details.
    :license: GNU GPL v3 or above, see LICENSE for more details.
"""


import logging

from dragonpy.core.configs import VECTREX, BaseConfig
from dragonpy.vectrex.mem_info import VectrexMemInfo
from dragonpy.vectrex.vectrex_rom import VectrexRom


log = logging.getLogger(__name__)


# from dragonlib.api import VectrexAPI
class VectrexCfg(BaseConfig):
    """
    http://www.playvectrex.com/designit/chrissalo/toc.htm

    $0000 - $7FFF Cartridge ROM
    $8000 - $C7FF Unmapped space
    $C800 - $CFFF RAM
    $D000 - $D7FF 6522 interface adapter
    $D800 - $DFFF 6522 / RAM ?!?
    $E000 - $EFFF ROM - builtin Mine storm game
    $F000 - $FFFF ROM - vectrex BIOS Executive
    """
    CONFIG_NAME = VECTREX
    MACHINE_NAME = "Vectrex"

    RAM_START = 0xC800
    RAM_END = 0xCFFF

    ROM_START = 0xE000
    ROM_END = 0xFFFF

    DEFAULT_ROMS = (
        VectrexRom(
            address=0xE000,
            # max_size=0x4000
        ),
    )

    # for unittests init:
    # STARTUP_END_ADDR = 0xbbe5 # scan keyboard

    def __init__(self, cmd_args):
        super().__init__(cmd_args)

        self.machine_api = None  # VectrexAPI()

        self.periphery_class = None  # VectrexPeriphery

        # TODO:
        # http://www.playvectrex.com/designit/chrissalo/appendixa.htm#Other
        if self.verbosity <= logging.ERROR:
            self.mem_info = VectrexMemInfo(log.debug)


config = VectrexCfg


# ------------------------------------------------------------------------------
