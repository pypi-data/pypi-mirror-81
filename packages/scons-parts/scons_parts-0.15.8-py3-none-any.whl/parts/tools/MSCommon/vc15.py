﻿

import os

import SCons.Platform
from parts.platform_info import SystemPlatform
from parts.tools.Common.Finders import (EnvFinder, PathFinder, RegFinder,
                                        ScriptFinder)
from parts.tools.Common.ToolInfo import ToolInfo

from .common import framework_root, framework_root64, get_current_sdk, msvc

# Need to verify the paths, but this seems to work well enough.

# version 15 .. 2017
# 32-bit
msvc.Register(
    hosts=[SystemPlatform('win32', 'any')],
    targets=[SystemPlatform('win32', 'x86')],
    info=[
        ToolInfo(
            version='15.0',
            install_scanner=[
                RegFinder([
                    r'Software\Wow6432Node\Microsoft\VisualStudio\SxS\VS7\15.0',
                    r'Software\Microsoft\VisualStudio\SxS\VS7\15.0',
                ]),
                PathFinder([
                    r'C:\Program Files (x86)\Microsoft Visual Studio\2017\Enterprise\VC',
                    r'C:\Program Files\Microsoft Visual Studio\2017\Enterprise\VC',
                    r'C:\Program Files (x86)\Microsoft Visual Studio\2017\Professional\VC',
                    r'C:\Program Files\Microsoft Visual Studio\2017\Professional\VC',
                    r'C:\Program Files (x86)\Microsoft Visual Studio\2017\Community\VC',
                    r'C:\Program Files\Microsoft Visual Studio\2017\Community\VC',
                ])
            ],
            script=ScriptFinder('${MSVC.VCINSTALL}/Auxiliary/Build/vcvarsall.bat', 'x86'),
            subst_vars={
                'VCINSTALL': '${MSVC.INSTALL_ROOT}/VC',
                'VSINSTALL': '${MSVC.INSTALL_ROOT}',
                'FRAMEWORK_ROOT': framework_root(),
                'FRAMEWORK_ROOT64': framework_root64()
            },
            shell_vars={},
            test_file='cl.exe'
        )
    ]
)

msvc.Register(
    hosts=[SystemPlatform('win32', 'x86_64')],
    targets=[SystemPlatform('win32', 'arm')],
    info=[
        ToolInfo(
            version='15.0',
            install_scanner=[
                RegFinder([
                    r'Software\Wow6432Node\Microsoft\VisualStudio\SxS\VS7\15.0',
                    r'Software\Microsoft\VisualStudio\SxS\VS7\15.0',
                ]),
                PathFinder([
                    r'C:\Program Files (x86)\Microsoft Visual Studio\2017\Enterprise\VC',
                    r'C:\Program Files\Microsoft Visual Studio\2017\Enterprise\VC',
                    r'C:\Program Files (x86)\Microsoft Visual Studio\2017\Professional\VC',
                    r'C:\Program Files\Microsoft Visual Studio\2017\Professional\VC',
                    r'C:\Program Files (x86)\Microsoft Visual Studio\2017\Community\VC',
                    r'C:\Program Files\Microsoft Visual Studio\2017\Community\VC',
                ])
            ],
            script=ScriptFinder('${MSVC.VCINSTALL}/Auxiliary/Build/vcvarsall.bat', 'amd64_arm'),
            subst_vars={
                'VCINSTALL': '${MSVC.INSTALL_ROOT}/VC',
                'VSINSTALL': '${MSVC.INSTALL_ROOT}',
                'FRAMEWORK_ROOT': framework_root(),
                'FRAMEWORK_ROOT64': framework_root64()
            },
            shell_vars={},
            test_file='cl.exe'
        )
    ]
)

msvc.Register(
    hosts=[SystemPlatform('win32', 'any')],
    targets=[SystemPlatform('win32', 'arm')],
    info=[
        ToolInfo(
            version='15.0',
            install_scanner=[
                RegFinder([
                    r'Software\Wow6432Node\Microsoft\VisualStudio\SxS\VS7\15.0',
                    r'Software\Microsoft\VisualStudio\SxS\VS7\15.0',
                ]),
                PathFinder([
                    r'C:\Program Files (x86)\Microsoft Visual Studio\2017\Enterprise\VC',
                    r'C:\Program Files\Microsoft Visual Studio\2017\Enterprise\VC',
                    r'C:\Program Files (x86)\Microsoft Visual Studio\2017\Professional\VC',
                    r'C:\Program Files\Microsoft Visual Studio\2017\Professional\VC',
                    r'C:\Program Files (x86)\Microsoft Visual Studio\2017\Community\VC',
                    r'C:\Program Files\Microsoft Visual Studio\2017\Community\VC',
                ])
            ],
            script=ScriptFinder('${MSVC.VCINSTALL}/Auxiliary/Build/vcvarsall.bat', 'x86_arm'),
            subst_vars={
                'VCINSTALL': '${MSVC.INSTALL_ROOT}/VC',
                'VSINSTALL': '${MSVC.INSTALL_ROOT}',
                'FRAMEWORK_ROOT': framework_root(),
                'FRAMEWORK_ROOT64': framework_root64()
            },
            shell_vars={},
            test_file='cl.exe'
        )
    ]
)

msvc.Register(
    hosts=[SystemPlatform('win32', 'x86_64')],
    targets=[SystemPlatform('win32', 'arm64')],
    info=[
        ToolInfo(
            version='15.0',
            install_scanner=[
                RegFinder([
                    r'Software\Wow6432Node\Microsoft\VisualStudio\SxS\VS7\15.0',
                    r'Software\Microsoft\VisualStudio\SxS\VS7\15.0',
                ]),
                PathFinder([
                    r'C:\Program Files (x86)\Microsoft Visual Studio\2017\Enterprise\VC',
                    r'C:\Program Files\Microsoft Visual Studio\2017\Enterprise\VC',
                    r'C:\Program Files (x86)\Microsoft Visual Studio\2017\Professional\VC',
                    r'C:\Program Files\Microsoft Visual Studio\2017\Professional\VC',
                    r'C:\Program Files (x86)\Microsoft Visual Studio\2017\Community\VC',
                    r'C:\Program Files\Microsoft Visual Studio\2017\Community\VC',
                ])
            ],
            script=ScriptFinder('${MSVC.VCINSTALL}/Auxiliary/Build/vcvarsall.bat', 'amd64_arm64'),
            subst_vars={
                'VCINSTALL': '${MSVC.INSTALL_ROOT}/VC',
                'VSINSTALL': '${MSVC.INSTALL_ROOT}',
                'FRAMEWORK_ROOT': framework_root(),
                'FRAMEWORK_ROOT64': framework_root64()
            },
            shell_vars={},
            test_file='cl.exe'
        )
    ]
)

msvc.Register(
    hosts=[SystemPlatform('win32', 'any')],
    targets=[SystemPlatform('win32', 'arm64')],
    info=[
        ToolInfo(
            version='15.0',
            install_scanner=[
                RegFinder([
                    r'Software\Wow6432Node\Microsoft\VisualStudio\SxS\VS7\15.0',
                    r'Software\Microsoft\VisualStudio\SxS\VS7\15.0',
                ]),
                PathFinder([
                    r'C:\Program Files (x86)\Microsoft Visual Studio\2017\Enterprise\VC',
                    r'C:\Program Files\Microsoft Visual Studio\2017\Enterprise\VC',
                    r'C:\Program Files (x86)\Microsoft Visual Studio\2017\Professional\VC',
                    r'C:\Program Files\Microsoft Visual Studio\2017\Professional\VC',
                    r'C:\Program Files (x86)\Microsoft Visual Studio\2017\Community\VC',
                    r'C:\Program Files\Microsoft Visual Studio\2017\Community\VC',
                ])
            ],
            script=ScriptFinder('${MSVC.VCINSTALL}/Auxiliary/Build/vcvarsall.bat', 'x86_arm64'),
            subst_vars={
                'VCINSTALL': '${MSVC.INSTALL_ROOT}/VC',
                'VSINSTALL': '${MSVC.INSTALL_ROOT}',
                'FRAMEWORK_ROOT': framework_root(),
                'FRAMEWORK_ROOT64': framework_root64()
            },
            shell_vars={},
            test_file='cl.exe'
        )
    ]
)

# 64-bit native
msvc.Register(
    hosts=[SystemPlatform('win32', 'x86_64')],
    targets=[SystemPlatform('win32', 'x86_64')],
    info=[
        ToolInfo(
            version='15.0',
            install_scanner=[
                RegFinder([
                    r'Software\Wow6432Node\Microsoft\VisualStudio\SxS\VS7\15.0',
                    r'Software\Microsoft\VisualStudio\SxS\VS7\15.0',
                ]),
                PathFinder([
                    r'C:\Program Files (x86)\Microsoft Visual Studio\2017\Enterprise\VC',
                    r'C:\Program Files\Microsoft Visual Studio\2017\Enterprise\VC',
                    r'C:\Program Files (x86)\Microsoft Visual Studio\2017\Professional\VC',
                    r'C:\Program Files\Microsoft Visual Studio\2017\Professional\VC',
                    r'C:\Program Files (x86)\Microsoft Visual Studio\2017\Community\VC',
                    r'C:\Program Files\Microsoft Visual Studio\2017\Community\VC',
                ])
            ],
            script=ScriptFinder('${MSVC.VCINSTALL}/Auxiliary/Build/vcvarsall.bat', 'amd64'),
            subst_vars={
                'VCINSTALL': '${MSVC.INSTALL_ROOT}/VC',
                'VSINSTALL': '${MSVC.INSTALL_ROOT}',
                'FRAMEWORK_ROOT': framework_root(),
                'FRAMEWORK_ROOT64': framework_root64()
            },
            shell_vars={},
            test_file='cl.exe'
        )
    ]
)

# cross - 64-bit.
msvc.Register(
    hosts=[SystemPlatform('win32', 'any')],
    targets=[SystemPlatform('win32', 'x86_64')],
    info=[
        ToolInfo(
            version='15.0',
            install_scanner=[
                RegFinder([
                    r'Software\Wow6432Node\Microsoft\VisualStudio\SxS\VS7\15.0',
                    r'Software\Microsoft\VisualStudio\SxS\VS7\15.0',
                ]),
                PathFinder([
                    r'C:\Program Files (x86)\Microsoft Visual Studio\2017\Enterprise\VC',
                    r'C:\Program Files\Microsoft Visual Studio\2017\Enterprise\VC',
                    r'C:\Program Files (x86)\Microsoft Visual Studio\2017\Professional\VC',
                    r'C:\Program Files\Microsoft Visual Studio\2017\Professional\VC',
                    r'C:\Program Files (x86)\Microsoft Visual Studio\2017\Community\VC',
                    r'C:\Program Files\Microsoft Visual Studio\2017\Community\VC',
                ])
            ],
            script=ScriptFinder('${MSVC.VCINSTALL}/Auxiliary/Build/vcvarsall.bat', 'x86_amd64'),
            subst_vars={
                'VCINSTALL': '${MSVC.INSTALL_ROOT}/VC',
                'VSINSTALL': '${MSVC.INSTALL_ROOT}',
                'FRAMEWORK_ROOT': framework_root(),
                'FRAMEWORK_ROOT64': framework_root64()
            },
            shell_vars={},
            test_file='cl.exe'
        )
    ]
)
