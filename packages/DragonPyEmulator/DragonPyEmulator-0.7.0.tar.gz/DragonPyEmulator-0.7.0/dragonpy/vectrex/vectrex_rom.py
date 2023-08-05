"""
    DragonPy - 6809 emulator in Python
    ==================================

    :created: 2015 by Jens Diemer - www.jensdiemer.de
    :copyleft: 2015 by the DragonPy team, see AUTHORS for more details.
    :license: GNU GPL v3 or above, see LICENSE for more details.
"""


import os

from dragonpy.components.rom import ROMFile


class VectrexRom(ROMFile):
    ROM_PATH = os.path.normpath(
        os.path.abspath(os.path.dirname(__file__))
    )
    SHA1 = "65d07426b520ddd3115d40f255511e0fd2e20ae7"
    FILENAME = "SYSTEM.IMG"

    def get_data(self):
        if not os.path.isfile(self.rom_path):
            raise RuntimeError(f"Rom file {self.rom_path!r} not there?!?")

        return super().get_data()
