import os
from platformio.platforms.base import BasePlatform


class SimplezPlatform(BasePlatform):
    """
    Simplez soft-processor is an open-source educational CISC processor.
    It only has 8 instructions, one register and 512 words of RAM. The
    instructions are 12 bits wide. It can be sintesithed on Lattice_ice40
    platforms
    """

    PACKAGES = {

        "toolchain-simplez": {

            # alias is used for quick access to package.
            "alias": "toolchain",

            # Flag which allows PlatformIO to install this package by
            # default via `> platformio install test` command
            "default": False
        },
    }

    def get_build_script(self):
            """ Returns a path to build script """

            # You can return static path
            # return "/path/to/test-builder.py"

            # or detect dynamically if `test-builder.py` is located in the same
            # folder with `test.py`
            return os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
                "simplez-builder.py"
            )
