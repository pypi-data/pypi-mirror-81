######################################
# g++ compiler configurations debug
######################################


from parts.config import *


def map_default_version(env):
    return env['GXX_VERSION']


config = configuration(map_default_version)

config.VersionRange("3-*",
                    append=ConfigValues(
                        CCFLAGS=['-O0', '-g'],
                        CPPDEFINES=['DEBUG']
                    )
                    )
