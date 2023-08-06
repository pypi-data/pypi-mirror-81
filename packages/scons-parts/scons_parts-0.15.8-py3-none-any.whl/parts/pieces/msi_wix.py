

import parts.api as api
import SCons.Script

# TODO need to add package group to scan directory
heat_action = SCons.Action.Action("heat.exe dir ${SOURCE} -o ${TARGET}"
                                  # -var var.PartsBuildDir"
                                  " -sw5150 -gg -cg ${TARGET.filebase}Group -srd -sfrag -dr INSTALLFOLDER"
                                  )

# internal wix package builder...
api.register.add_builder('_heat', SCons.Builder.Builder(
    action=heat_action,
    source_factory=SCons.Node.FS.Dir,
    source_scanner=SCons.Defaults.DirScanner,
    suffix='.wxs',
))
