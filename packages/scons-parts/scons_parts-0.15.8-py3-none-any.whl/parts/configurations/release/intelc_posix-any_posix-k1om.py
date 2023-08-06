######################################
# K1OM compiler configurations defaults for release
######################################


import sys

import SCons.Script
from parts.config import *


def map_default_version(env):
    return env['INTELC_VERSION']


config = configuration(map_default_version)


config.VersionRange("13-*",
                    append=ConfigValues(
                        CCFLAGS=['-O2'],
                        LINKFLAGS=['-static-intel'],
                    )
                    )
