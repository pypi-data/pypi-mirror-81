######################################
# as compiler configurations default
######################################


from parts.config import *


def map_default_version(env):
    return env['GXX_VERSION']


config = configuration(map_default_version)

config.VersionRange("*",
                    replace=ConfigValues(
                        PROGSUFFIX='',
                        INSTALL_BIN_PATTERN=['*'],
                        SDK_BIN_PATTERN=['*'],
                        # setup linux paths in tmp files
                        CXXCOM='${TEMPFILE("$CXX -o $TARGET -c $CXXFLAGS $CCFLAGS $_CCCOMCOM $SOURCES",force_posix_paths=True)}',
                        SHCXXCOM='${TEMPFILE("$SHCXX -o $TARGET -c $SHCXXFLAGS $SHCCFLAGS $_CCCOMCOM $SOURCES",force_posix_paths=True)}',
                    ),
                    )
