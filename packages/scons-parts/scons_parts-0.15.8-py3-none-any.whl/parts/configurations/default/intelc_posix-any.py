######################################
# Intel compiler configurations default-posix
######################################


import os

from parts.config import *


def make_bool(obj):
    if obj is bool():
        return obj
    # assume string
    if obj.lower() == 'true':
        return True
    return False


def map_default_version(env):
    return env['INTELC_VERSION']


def post_process_func(env):
    try:
        env['GCC'].VERSION
    except (AttributeError, KeyError):
        raise RuntimeError("You need to define gnutools or compatible tool chain with Intel tool chain")

    env.AppendUnique(CCFLAGS=['-gcc-name=${GCC.TOOL}', '-gxx-name=${GXX.TOOL}'] + (
        # -gcc-version is deprecated in 13.1, use it only for older compilers
        env['INTELC_VERSION'] < '13.1' and ['-gcc-version=${"".join(str(GCC.VERSION).split("."))}'] or []))

    # code coverage feature additions
    if make_bool(env.get('codecov', False)) == True:
        if(env.Version(env['INTELC_VERSION']) >= 11):
            env.AppendUnique(CCFLAGS=['-prof-gen=srcpos'])
        else:
            env.AppendUnique(CCFLAGS=['-prof-genx'])


config = configuration(map_default_version, post_process_func)

config.VersionRange(
    "*",
    # RUN_PATH setting for this platform toolchain
    replace=ConfigValues(
        _RPATHSTR='${JOIN("$RUNPATHS",":")}',
        RPATHLINK=[],
        _RPATHLINK='${_concat("-Wl,-rpath-link=", RPATHLINK, "", __env__, RDirs, TARGET, SOURCE)}',
        _ABSRPATHLINK='${_concat("-Wl,-rpath-link=", RPATHLINK, "", __env__, ABSDir, TARGET, SOURCE)}',
        _RUNPATH='${_concat(RPATHPREFIX, _RPATHSTR, RPATHSUFFIX, __env__)}',
        _RPATH='$_RUNPATH $_RPATHLINK',
        _ABSRPATH='$_RUNPATH $_ABSRPATHLINK',
        RUNPATHS='${GENRUNPATHS()}',
        RPATHSUFFIX=",--enable-new-dtags",
    ),
)
