# this overide deals with Part providing better information for what there is a duplicated
# target/environment/builder being reproted by SCons. This allows Part to report which two
# Parts are the issues, which helps a lot when this happens across parts, as the SCons
# message is hard to deal with by default and it does not know of "part/components"
# We also make what Component "owns" these node for faster checks latter.


import parts.api as api
import parts.errors as errors
import parts.glb as glb
import parts.metatag as metatag
import SCons.Builder

scons_node_errors = SCons.Builder._node_errors


def parts_node_errors(builder, env, tlist, slist):
    """SCons errors out without a lot of useful info
    This function tries to do the same tests, but report more useful stuff given that we have components
    """

    #print("source:", [str(i) for i in slist])
    #print("target:", [str(i) for i in tlist])
    pobj = glb.engine._part_manager._from_env(env)
    if pobj:
        tag_part_info(tlist + slist, pobj)
        pobj.DefiningSection.Targets.extend(tlist)
        pobj.DefiningSection.Sources.extend(slist)

    # make sure we can record that nodes before we stop SCons registering the values here
    # we throw an exception to allow Parts to handle the allow_duplicate feature for all builders
    if env.get('_found_duplication'):
        raise errors.AllowedDuplication()

    error = False
    warn = False
    # use basic SCons template for how it handles these error.. may append on to later
    for t in tlist:
        if t.side_effect:
            error = True
        if t.has_explicit_builder():
            if not t.env is None and not t.env is env:
                action = t.builder.action
                t_contents = action.get_contents(tlist, slist, t.env)
                contents = action.get_contents(tlist, slist, env)
                if t_contents == contents:
                    warn = True
                else:
                    error = True
            if builder.multi:
                if t.get_executor() is None:
                    api.output.warning_msg(
                        "Executor is None for node '{}'.\n This is a sign that there is a order dependancy that is incorrect in the mutli builder used to generate this target".format(t.ID), show_stack=False)
                    del t.executor
                if t.get_executor() and (t.builder != builder or t.get_executor().get_all_targets() != tlist):
                    error = True
            elif t.sources != slist:
                error = True

        if error:
            tenv = {} if t.env is None else t.env
            api.output.error_msg(
                '{0} is ambiguous because it is defined with two different Environments\n One environment was defined in Part "{1}"\n The other was defined in Part "{2}"'.format(
                    t, tenv.get(
                        'PART_ALIAS', "<unknown>"), env.get(
                        'PART_ALIAS', "<unknown>")), show_stack=False, exit=False)
        elif warn:
            api.output.warning_msg(
                'Build issue found with two different Environments\n One environment was defined in Part "%s"\n The other was defined in Part "%s"' %
                (t.env.get(
                    'PART_ALIAS', "<unknown>"), env.get(
                    'PART_ALIAS', "<unknown>")), show_stack=False)

    # call the SCons code
    scons_node_errors(builder, env, tlist, slist)


SCons.Builder._node_errors = parts_node_errors

# util function


def tag_part_info(node_list, pobj):
    for node in node_list:
        alias = pobj.Alias
        section = pobj.DefiningSection
        data = metatag.MetaTagValue(node, 'components', ns='partinfo', default={})

        # Tag this node with information about the Parts and Section that would care about it
        data.setdefault(alias, set()).add(section)

        metatag.MetaTag(node, 'partinfo', components=data)

        # Tag Parent Directory nodes
        if isinstance(node, SCons.Node.FS.Base):
            if isinstance(node, SCons.Node.FS.Entry):
                dnode = node.get_dir()
            else:
                dnode = node.Dir('.')
            while True:

                data = metatag.MetaTagValue(dnode, 'components', ns='partinfo', default={})
                # check to see if this directory has this information already
                # if so we can exit
                sections = data.setdefault(alias, set())
                if section in sections:
                    break

                sections.add(section)
                metatag.MetaTag(dnode, 'partinfo', components=data)

                if dnode == dnode.Dir('..'):
                    break
                dnode = dnode.Dir('..')
