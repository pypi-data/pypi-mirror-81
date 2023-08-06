
import json

import parts.api as api
import parts.glb as glb
import parts.common as common
import parts.packaging as packaging
import parts.core.util as util
import parts.node_helpers as node_helpers
import parts.core.builders as builders
import SCons.Script
from SCons.Script.SConscript import SConsEnvironment
##################################
# defines two builders
#
# one builder is the builder that generated a json file
# that contains all the installed files sort package group
# This is used as sync point in the depends tree for dynamic
# builders that would install items.
#
# the second builder is generates a json file for a given package group
#
# ideal in both cases I think this could be done with Value node
# given they are fixed a little. This would be better as the information
# would be in memory and I would not need to create a set of files

global_file_name = "$PARTS_SYS_DIR/package.groups.jsn"

# the wrapper function


def DynamicPackageNodes(_env, source):
    '''
    This file defines all the files that will be packagable for any given group
    It is in the depend chain for creating any package that we need to generate
    '''
    # make sure we have a common environment for this mutli build
    # is it needs to be defined at a "global" level
    env = glb.engine.def_env
    # this defines the
    targets = env._DynamicPackageNodes(global_file_name, source)
    # we set a special decider to make sure item that depend on this
    # will rebuild. This is needed at the moment as the json file does not
    # contain information about the "csig" of any files it has. Given this a
    # a content change will not be seen and as such the package builder will
    # not rebuild adding updated nodes into the package.
    # todo change the json file to have csig info to make sure packages rebuild
    # only when they are changed

    return targets


def WritePackageGroupFiles(target, source, env):
    # This write out all the files that would be install
    # orginized by the groups
    with open(target[0].get_path(), 'w') as outfile:
        data = json.dumps(
            dict(
                pkg=packaging._sorted_groups[0],
                no_pkg=packaging._sorted_groups[1]
            ),
            indent=2,
            cls=util.SetNodeEncode
        )
        outfile.write(data)


def target_scanner(node, env, path):
    # clear any cached data as regen file list
    # should only need to be called here as after this target is called we should have
    # called all "installXXX" functions that would define a node to install
    if not node_helpers.has_children_changed(node):
        api.output.verbose_msg(["dynamicpackage-scanner", "scanner", "scanner-called"], "called {}".format(node.ID))
        packaging.SortPackageGroups()
        packaging._sorted_groups
    return []


# this allow us to define a "dynamic" value that will have to be build
# before we try to get nodes for a given group. This is call via a wrapper
# to ensure a common environment
api.register.add_builder('_DynamicPackageNodes', SCons.Builder.Builder(
    action=SCons.Action.Action(WritePackageGroupFiles, "Sync any dynamic builders with node that need to be packaged"),
    target_factory=SCons.Node.FS.File,
    source_factory=SCons.Node.FS.File,
    target_scanner=SCons.Script.Scanner(target_scanner),
    multi=1
))

###########################################################################
###########################################################################

# the wrapper function


def GroupBuilder(env, source, no_pkg=False, **kw):
    '''
    This builder will make a json file and set some node values for 
    a given package group. It will depend on the "master" dynamic.package.jsn
    file that will contain a all the package files and group that are defined
    '''

    # make sure we have a common environment for this mutli build
    # is it needs to be defined at a "global" level
    nenv = glb.engine.def_env
    out = nenv._GroupBuilder(
        target=source,
        source=[],
        allow_duplicates=True,
        _local_export_file=env.subst(builders.exports.file_name),
        **kw
    )

    return out


def GroupBuilderAction(target, source, env):
    # get the group name from the target file name
    
    group_name = ".".join(target[0].name.split(".")[2:-1])
    
    new_sources, no_pkg = env.GetFilesFromPackageGroups(target, [group_name])
    if not env.get("no_pkg", False):
        target[0].attributes.GroupFiles = new_sources
    else:
        target[0].attributes.GroupFiles = no_pkg

    with open(target[0].get_path(), 'w') as outfile:
        tt = [{"name": i.ID, "type": util.json_type(i)} for i in target[0].attributes.GroupFiles]
        data = json.dumps(tt, indent=2,)
        outfile.write(data)


def emit(target, source, env):
    # need to be absolute on the path as the VariantDir() is a global value
    # that effect everything, it is not per environment
    ret = []
    for trg in target:
        trg = env.File("${{PARTS_SYS_DIR}}/package.group.{}.jsn".format(trg.ID))
        ret.append(trg)
    return ret, source


def GroupNodesScanner(node, env, path):

    api.output.verbose_msg(["groupbuilder-scanner", "scanner", "scanner-called"], "called {}".format(node.ID))

    # This is the default group we depend on unless the node has a meta value saying that this
    # can be defined on the export.jsn file of this part instead. This can prevent the building of all
    # components that are doing dynamic build action before this file can be generated correctly.
    local = env.MetaTagValue(node, 'local_group', 'parts', False)
    if local:
        api.output.verbose_msg(["groupbuilder-scanner", "scanner"], "Mapping {} as local".format(node.ID))
        ret = [env.File(env['_local_export_file'])]
    else:
        api.output.verbose_msg(["groupbuilder-scanner", "scanner"], "Mapping {} as global".format(node.ID))
        ret = [env.File(global_file_name)]

    # make sure the groups are sorted
    # We want to check the export file added above for changes
    # to decide if we will add the sources at this point in time
    if not node_helpers.has_changed(ret[0]):
        node = ".".join(node.name.split(".")[2:-1])
        new_sources, _ = env.GetFilesFromPackageGroups("", [node])
        ret += new_sources

    api.output.verbose_msgf(["groupbuilder-scanner", "scanner"], "Returned {}", common.DelayVariable(lambda: [i.ID for i in ret]))
    return ret

#".".join(target[0].name.split(".")[2:-1])
api.register.add_builder('_GroupBuilder', SCons.Builder.Builder(
    action=SCons.Action.Action(GroupBuilderAction, "Looking up files in package group '${'.'.join(TARGET.name.split(\'.\')[2:-1])}'"),
    target_factory=SCons.Node.FS.File,
    source_factory=SCons.Node.Python.Value,
    emitter=emit,
    target_scanner=SCons.Script.Scanner(GroupNodesScanner),
))

SConsEnvironment.GroupBuilder = GroupBuilder
SConsEnvironment.DynamicPackageNodes = DynamicPackageNodes
