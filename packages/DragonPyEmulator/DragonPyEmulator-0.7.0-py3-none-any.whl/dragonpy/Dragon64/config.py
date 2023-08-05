"""
    Dragon 64 config
    ================

    :created: 2014 by Jens Diemer - www.jensdiemer.de
    :copyleft: 2014-2015 by the DragonPy team, see AUTHORS for more details.
    :license: GNU GPL v3 or above, see LICENSE for more details.
"""


import logging

from dragonpy.core.configs import DRAGON64
from dragonpy.Dragon32.config import Dragon32Cfg
from dragonpy.Dragon64.Dragon64_rom import Dragon64RomIC17, Dragon64RomIC18
from dragonpy.Dragon64.mem_info import get_dragon_meminfo


class Dragon64Cfg(Dragon32Cfg):
    CONFIG_NAME = DRAGON64
    MACHINE_NAME = "Dragon 64"

    RAM_START = 0x0000

    # 1KB RAM is not runnable and raise a error
    # 2-8 KB - BASIC Interpreter will be initialized. But every
    #          statement will end with a OM ERROR (Out of Memory)
    # 16 KB - Is usable

#     RAM_END = 0x03FF # 1KB
#     RAM_END = 0x07FF # 2KB # BASIC will always raise a OM ERROR!
#     RAM_END = 0x0FFF # 4KB # BASIC will always raise a OM ERROR!
#     RAM_END = 0x1FFF # 8KB # BASIC will always raise a OM ERROR!
#     RAM_END = 0x3FFF # 16KB # usable
    RAM_END = 0x7FFF  # 32KB

    ROM_START = 0x8000
    ROM_END = 0xFFFF
    # ROM size: 0x8000 == 32768 Bytes

    """
    $8000-$bfff - d64_ic17.rom - size: $3fff (dez.: 16383) Bytes
    $c000-$ffff - d64_ic18.rom - size: $3fff (dez.: 16383) Bytes
    """
    DEFAULT_ROMS = (
        Dragon64RomIC17(address=0x8000, max_size=0x4000),
        Dragon64RomIC18(address=0xC000, max_size=0x4000),
    )

    def __init__(self, cmd_args):
        super().__init__(cmd_args)

        if self.verbosity <= logging.ERROR:
            self.mem_info = get_dragon_meminfo()

        self.periphery_class = None  # Dragon32Periphery

    def get_initial_RAM(self):
        """
        init the Dragon RAM
        See: http://archive.worldofdragon.org/phpBB3/viewtopic.php?f=5&t=4444
        """
        mem_FF = [0xff for _ in range(4)]
        mem_00 = [0x00 for _ in range(4)]

        mem = []
        for _ in range(self.RAM_SIZE // 8):
            mem += mem_FF
            mem += mem_00

        return mem


config = Dragon64Cfg
