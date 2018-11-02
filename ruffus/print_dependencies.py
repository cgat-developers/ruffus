################################################################################
#
#   print_dependencies.py
#
#
#   Copyright (c) 10/9/2009 Leo Goodstadt
#
#   Permission is hereby granted, free of charge, to any person obtaining a copy
#   of this software and associated documentation files (the "Software"), to deal
#   in the Software without restriction, including without limitation the rights
#   to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#   copies of the Software, and to permit persons to whom the Software is
#   furnished to do so, subject to the following conditions:
#
#   The above copyright notice and this permission notice shall be included in
#   all copies or substantial portions of the Software.
#
#   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#   IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#   FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#   AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#   LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#   OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#   THE SOFTWARE.
#################################################################################
from collections import defaultdict
from .adjacent_pairs_iterate import adjacent_pairs_iterate
"""
    print_dependencies.py

        provides support for dependency trees

"""

#
#   Number of pre-canned colour schemes
#
CNT_COLOUR_SCHEMES = 8


try:
    from StringIO import StringIO
except:
    from io import StringIO


def _get_name(node):
    """
    Get name for node
        use display_name or _name
    """
    if hasattr(node, "display_name"):
        return node.display_name
    elif hasattr(node, "_name"):
        return node._name
    else:
        raise Exception(
            "Unknown node type [%s] has neither _name or display_name" % str(node))


def attributes_to_str(attributes, name):
    """
    helper function for dot format
    turns dictionary into a=b, c=d...
    """

    # remove ugly __main__. qualifier
    name = name.replace("__main__.", "")

    # if a label is specified, that overrides the node name
    if "label" not in attributes:
        attributes["label"] = name.replace(
            "  before ", "\\nbefore ").replace(",  ", ",\n")

    # remove any quotes
    if attributes["label"][0] == '<':
        attributes["label"] = attributes["label"][1:-1]
        html_label = True
    else:
        html_label = False
        if attributes["label"][0] == '"':
            attributes["label"] = attributes["label"][1:-1]

    # add suffix / prefix
    if "label_prefix" in attributes:
        attributes["label"] = attributes["label_prefix"] + attributes["label"]
        del attributes["label_prefix"]
    if "label_suffix" in attributes:
        attributes["label"] = attributes["label"] + attributes["label_suffix"]
        del attributes["label_suffix"]

    # restore quotes
    if html_label:
        attributes["label"] = '<' + attributes["label"] + '>'
    else:
        attributes["label"] = '"' + attributes["label"] + '"'

    # support for html labels
    # if "<" in name and ">" in name:
    #    attributes["label"] = '<' + name + '>'
    # else:
    #    attributes["label"] = '"' + name + '"'

    return "[" + ", ".join("%s=%s" % (k, v) for k, v in sorted(attributes.items())) + "];\n"


# _________________________________________________________________________________________
#
#   get_arrow_str_for_legend_key
# _________________________________________________________________________________________
def get_arrow_str_for_legend_key(from_task_type, to_task_type, n1, n2, colour_scheme):
    """
    Get dot format for arrows inside legend key
    """
    if "Vicious cycle" in (from_task_type, to_task_type):
        return ("%s -> %s[color=%s, arrowtype=normal];\n" % (n1, n2, colour_scheme["Vicious cycle"]["linecolor"]) +
                "%s -> %s[color=%s, arrowtype=normal];\n" % (n2, n1, colour_scheme["Vicious cycle"]["linecolor"]))
    if from_task_type in ("Final target", "Task to run",
                          "Up-to-date task forced to rerun",
                          "Explicitly specified task"):
        return "%s -> %s[color=%s, arrowtype=normal];\n" % (n1, n2, colour_scheme["Task to run"]["linecolor"])
    elif from_task_type in ("Up-to-date task", "Down stream", "Up-to-date Final target"):
        return "%s -> %s[color=%s, arrowtype=normal];\n" % (n1, n2, colour_scheme["Up-to-date"]["linecolor"])
    #
    # shouldn't be here!!
    #
    else:
        return "%s -> %s[color=%s, arrowtype=normal];\n" % (n1, n2, colour_scheme["Up-to-date"]["linecolor"])


# _________________________________________________________________________________________
#
#   get_default_colour_scheme
# _________________________________________________________________________________________
def get_default_colour_scheme(default_colour_scheme_index=0):
    """
    A selection of default colour schemes "inspired" by entries in
        http://kuler.adobe.com/#create/fromacolor
    """

    if default_colour_scheme_index == 0:
        bluey_outline = '"#0044A0"'
        bluey = '"#EBF3FF"'
        greeny_outline = '"#006000"'
        greeny = '"#B8CC6E"'
        orangey = '"#EFA03B"'
        orangey_outline = greeny_outline
        ruddy = '"#FF3232"'
    elif default_colour_scheme_index == 1:
        bluey_outline = '"#000DDF"'
        bluey = 'transparent'
        greeny_outline = '"#4B8C2E"'
        greeny = '"#9ED983"'
        orangey = '"#D98100"'
        orangey_outline = '"#D9D911"'
        ruddy = '"#D93611"'
    elif default_colour_scheme_index == 2:
        bluey_outline = '"#4A64A5"'
        bluey = 'transparent'
        greeny_outline = '"#4A92A5"'
        greeny = '"#99D1C1"'
        orangey = '"#D2C24A"'
        orangey_outline = greeny_outline
        ruddy = '"#A54A64"'
    elif default_colour_scheme_index == 3:
        bluey_outline = '"#BFB5FF"'
        bluey = 'transparent'
        greeny_outline = '"#7D8A2E"'
        greeny = '"#C9D787"'
        orangey = '"#FFF1DC"'
        orangey_outline = greeny_outline
        ruddy = '"#FF3E68"'
    elif default_colour_scheme_index == 4:
        bluey_outline = '"#004460"'
        bluey = 'transparent'
        greeny_outline = '"#4B6000"'
        greeny = '"#B8CC6E"'
        orangey = '"#FFF0A3"'
        orangey_outline = greeny_outline
        ruddy = '"#F54F29"'
    elif default_colour_scheme_index == 5:
        bluey_outline = '"#1122FF"'
        bluey = '"#AABBFF"'
        greeny_outline = '"#007700"'
        greeny = '"#44FF44"'
        orangey = '"#EFA03B"'
        orangey_outline = '"#FFCC3B"'
        ruddy = '"#FF0000"'
    elif default_colour_scheme_index == 6:
        bluey_outline = '"#0044A0"'
        bluey = '"#EBF3FF"'
        greeny_outline = 'black'
        greeny = '"#6cb924"'
        orangey = '"#ece116"'
        orangey_outline = greeny_outline
        ruddy = '"#FF3232"'
    else:
        bluey_outline = '"#87BAE4"'
        bluey = 'transparent'
        greeny_outline = '"#87B379"'
        greeny = '"#D3FAE3"'
        orangey = '"#FDBA40"'
        orangey_outline = greeny_outline
        ruddy = '"#b9495e"'
    default_colour_scheme = defaultdict(dict)
    default_colour_scheme["Vicious cycle"]["linecolor"] = ruddy
    default_colour_scheme["Pipeline"]["fontcolor"] = ruddy
    default_colour_scheme["Key"]["fontcolor"] = "black"
    default_colour_scheme["Key"]["fillcolor"] = '"#F6F4F4"'
    default_colour_scheme["Task to run"]["linecolor"] = bluey_outline
    default_colour_scheme["Up-to-date"]["linecolor"] = "gray"
    default_colour_scheme["Final target"]["fillcolor"] = orangey
    default_colour_scheme["Final target"]["fontcolor"] = "black"
    default_colour_scheme["Final target"]["color"] = "black"
    default_colour_scheme["Final target"]["dashed"] = 0
    default_colour_scheme["Vicious cycle"]["fillcolor"] = ruddy
    default_colour_scheme["Vicious cycle"]["fontcolor"] = 'white'
    default_colour_scheme["Vicious cycle"]["color"] = "white"
    default_colour_scheme["Vicious cycle"]["dashed"] = 0
    default_colour_scheme["Up-to-date task"]["fillcolor"] = greeny
    default_colour_scheme["Up-to-date task"]["fontcolor"] = greeny_outline
    default_colour_scheme["Up-to-date task"]["color"] = greeny_outline
    default_colour_scheme["Up-to-date task"]["dashed"] = 0
    default_colour_scheme["Down stream"]["fillcolor"] = "white"
    default_colour_scheme["Down stream"]["fontcolor"] = "gray"
    default_colour_scheme["Down stream"]["color"] = "gray"
    default_colour_scheme["Down stream"]["dashed"] = 0
    default_colour_scheme["Explicitly specified task"]["fillcolor"] = "transparent"
    default_colour_scheme["Explicitly specified task"]["fontcolor"] = "black"
    default_colour_scheme["Explicitly specified task"]["color"] = "black"
    default_colour_scheme["Explicitly specified task"]["dashed"] = 0
    default_colour_scheme["Task to run"]["fillcolor"] = bluey
    default_colour_scheme["Task to run"]["fontcolor"] = bluey_outline
    default_colour_scheme["Task to run"]["color"] = bluey_outline
    default_colour_scheme["Task to run"]["dashed"] = 0
    default_colour_scheme["Up-to-date task forced to rerun"]["fillcolor"] = 'transparent'
    default_colour_scheme["Up-to-date task forced to rerun"]["fontcolor"] = bluey_outline
    default_colour_scheme["Up-to-date task forced to rerun"]["color"] = bluey_outline
    default_colour_scheme["Up-to-date task forced to rerun"]["dashed"] = 1
    default_colour_scheme["Up-to-date Final target"]["fillcolor"] = orangey
    default_colour_scheme["Up-to-date Final target"]["fontcolor"] = orangey_outline
    default_colour_scheme["Up-to-date Final target"]["color"] = orangey_outline
    default_colour_scheme["Up-to-date Final target"]["dashed"] = 0

    if default_colour_scheme_index == 6:
        default_colour_scheme["Vicious cycle"]["fontcolor"] = 'black'
        default_colour_scheme["Task to run"]["fillcolor"] = '"#5f52ee"'
        default_colour_scheme["Task to run"]["fontcolor"] = "lightgrey"
        default_colour_scheme["Up-to-date Final target"]["fontcolor"] = '"#EFA03B"'

    return default_colour_scheme


# _________________________________________________________________________________________
#
#   get_dot_format_for_task_type
# _________________________________________________________________________________________
def get_dot_format_for_task_type(task_type, attributes, colour_scheme, used_formats):
    """
    Look up appropriate colour and style for each type of task
    """
    used_formats.add(task_type)
    for color_type in ("fontcolor", "fillcolor", "color"):
        attributes[color_type] = colour_scheme[task_type][color_type]
        attributes["style"] = "filled"
        if colour_scheme[task_type]["dashed"]:
            attributes["style"] = "dashed"


# _________________________________________________________________________________________
#
#   write_legend_key
# _________________________________________________________________________________________
def write_legend_key(stream, used_task_types, minimal_key_legend, colour_scheme, key_name="Key:", subgraph_index=1):
    """
    Write legend/key to dependency tree graph
    """
    if not len(used_task_types):
        return

    stream.write('subgraph clusterkey%d\n' % subgraph_index)
    stream.write('{\n')

    stream.write('rank="min";\n')
    stream.write('style=filled;\n')
    stream.write('fontsize=20;\n')
    stream.write('color=%s;\n' % (colour_scheme["Key"]["fillcolor"]))
    stream.write('label = "%s";\n' % key_name)
    stream.write('fontcolor = %s;' % (colour_scheme["Key"]["fontcolor"]))
    stream.write('node[margin="0.2,0.2", fontsize="14"];\n')

    #
    #   Only include used task types
    #
    all_task_types = [
        "Vicious cycle",
        "Down stream",
        "Up-to-date task",
        "Explicitly specified task",
        "Task to run",
        "Up-to-date task forced to rerun",
        "Up-to-date Final target",
        "Final target", ]
    if not minimal_key_legend:
        used_task_types |= set(all_task_types)
    wrapped_task_types = [
        "Vicious cycle",
        "Down stream",
        "Up-to-date task",
        "Explicitly specified task",
        "Task to run",
        "Up-to-date task\\nforced to rerun",
        "Up-to-date\\nFinal target",
        "Final target", ]
    wrapped_task_types = dict(zip(all_task_types, wrapped_task_types))

    def outputkey(key, task_type, stream):
        ignore_used_task_types = set()
        attributes = dict()
        attributes["shape"] = "box3d"
        #attributes["shape"] = "rect"
        get_dot_format_for_task_type(
            task_type, attributes, colour_scheme, ignore_used_task_types)
        #attributes["fontsize"] = '15'
        stream.write(key + attributes_to_str(attributes,
                                             wrapped_task_types[task_type]))

    sorted_used_task_types = []
    for t in all_task_types:
        if t in used_task_types:
            sorted_used_task_types.append(t)

    # print first key type
    outputkey("k1_%d" % subgraph_index, sorted_used_task_types[0], stream)

    for i, (from_task_type, to_task_type) in enumerate(adjacent_pairs_iterate(sorted_used_task_types)):
        from_key = 'k%d_%d' % (i + 1, subgraph_index)
        to_key = 'k%d_%d' % (i + 2, subgraph_index)
        # write key
        outputkey(to_key, to_task_type, stream)
        # connection between keys
        stream.write(get_arrow_str_for_legend_key(from_task_type,
                                                  to_task_type, from_key, to_key, colour_scheme))

    stream.write("}\n")


# _________________________________________________________________________________________

#   write_colour_scheme_demo_in_dot_format

# _________________________________________________________________________________________
def write_colour_scheme_demo_in_dot_format(stream):
    """
    Write all the colour schemes in different colours
    """
    stream.write('digraph "Colour schemes"\n{\n')
    stream.write('size="8,11";\n')
    stream.write('splines=true;\n')
    stream.write('fontsize="30";\n')
    stream.write('ranksep = 0.3;\n')
    stream.write('node[fontsize="20"];\n')
    for colour_scheme_index in range(CNT_COLOUR_SCHEMES):
        colour_scheme = get_default_colour_scheme(colour_scheme_index)
        write_legend_key(stream, set("test"), False, colour_scheme,
                         "Colour Scheme %d" % colour_scheme_index, colour_scheme_index)
    stream.write("}\n")


# _________________________________________________________________________________________

#   write_flowchart_in_dot_format

# _________________________________________________________________________________________
def write_flowchart_in_dot_format(jobs_to_run,
                                  up_to_date_jobs,
                                  dag_violating_edges,
                                  dag_violating_nodes,
                                  byte_stream,
                                  target_jobs,
                                  forced_to_run_jobs=[],
                                  all_jobs=None,
                                  vertical=True,
                                  skip_uptodate_tasks=False,
                                  no_key_legend=False,
                                  minimal_key_legend=True,
                                  user_colour_scheme=None,
                                  pipeline_name="Pipeline:"):
    """
    jobs_to_run         = pipeline jobs which are not up to date or have dependencies
                            which are not up to date

    vertical            = print flowchart vertically
    minimal_key_legend  = only print used task types in key legend
    user_colour_scheme  = dictionary for overriding default colours
                          Colours can be names e.g. "black" or quoted hex e.g. '"#F6F4F4"'
                          Default values will be used unless specified

                          key    = "colour_scheme_index": index of default colour scheme
                          key    = "Final target"
                                   "Explicitly specified task"
                                   "Task to run"
                                   "Down stream"
                                   "Up-to-date Final target"
                                   "Up-to-date task forced to rerun"
                                   "Up-to-date task"
                                   "Vicious cycle"
                                   Specifies colours for each task type

                              Subkey = "fillcolor"
                                       "fontcolor"
                                       "color"
                                       "dashed"   = 0/1


                          key    =  "Vicious cycle"
                                    "Task to run"
                                    "Up-to-date"

                              Subkey = "linecolor"
                                       Specifying colours for arrows between tasks

                          key    = "Pipeline"

                              Subkey = "fontcolor"
                                        Specifying flowchart title colour

                          key    = "Key"

                              Subkey = "fontcolor"
                                       "fillcolor"
                                       Specifies legend colours
    """

    if user_colour_scheme is None:
        colour_scheme = get_default_colour_scheme()
    else:
        if "colour_scheme_index" in user_colour_scheme:
            colour_scheme_index = user_colour_scheme["colour_scheme_index"]
        else:
            colour_scheme_index = 0
        colour_scheme = get_default_colour_scheme(colour_scheme_index)
        for k, v in user_colour_scheme.items():
            if k not in colour_scheme:
                continue
            if isinstance(v, dict):
                colour_scheme[k].update(v)
            else:
                colour_scheme[k] = v

    up_to_date_jobs = set(up_to_date_jobs)

    #
    #   cases where child points back to ancestor
    #
    dag_violating_dependencies = set(dag_violating_edges)

    stream = StringIO()

    stream.write('digraph "%s"\n{\n' % pipeline_name)
    stream.write('size="8,11";\n')
    stream.write('splines=true;\n')
    stream.write('fontsize="30";\n')
    stream.write('ranksep = 0.3;\n')
    stream.write('node[fontsize="20"];\n')
    stream.write('graph[clusterrank="local"];\n')

    if not vertical:
        stream.write('rankdir="LR";\n')
    stream.write('subgraph clustertasks\n'
                 "{\n")
    stream.write('rank="min";\n')
    stream.write('fontcolor = %s;\n' % colour_scheme["Pipeline"]["fontcolor"])
    stream.write('label = "%s";\n' % pipeline_name)
    # if vertical:
    #    stream.write( 'edge[minlen=2];\n')
    delayed_task_strings = list()
    vicious_cycle_task_strings = list()

    #
    #   all jobs should be specified
    #       this is a bad fall-back
    #       because there is no guarantee that we are printing what we want to print
    if all_jobs is None:
        all_jobs = node.all_nodes

    used_task_types = set()

    #
    #   defined duplicately in graph. Bad practice
    #
    _one_to_one = 0
    _many_to_many = 1
    _one_to_many = 2
    _many_to_one = 3

    for n in all_jobs:
        attributes = dict()
        attributes["shape"] = "box3d"
        #attributes["shape"] = "rect"
        if hasattr(n, "single_multi_io"):
            if n.single_multi_io == _one_to_many:
                attributes["shape"] = "house"
                attributes["peripheries"] = 2
            elif n.single_multi_io == _many_to_one:
                attributes["shape"] = "invhouse"
                attributes["height"] = 1.1
                attributes["peripheries"] = 2

        #
        #   circularity violating DAG: highlight in red
        #
        if n in dag_violating_nodes:
            get_dot_format_for_task_type(
                "Vicious cycle", attributes, colour_scheme, used_task_types)
            vicious_cycle_task_strings.append(
                't%d' % n._node_index + attributes_to_str(attributes, _get_name(n)))
        #
        #   these jobs will be run
        #
        elif n in jobs_to_run:

            #
            #   up to date but forced to run: outlined in blue
            #
            if n in forced_to_run_jobs:
                get_dot_format_for_task_type(
                    "Explicitly specified task", attributes, colour_scheme, used_task_types)

            #
            #   final target: outlined in orange
            #
            elif n in target_jobs:
                get_dot_format_for_task_type(
                    "Final target", attributes, colour_scheme, used_task_types)

            #
            #   up to date dependency but forced to run: outlined in green
            #
            elif n in up_to_date_jobs:
                get_dot_format_for_task_type(
                    "Up-to-date task forced to rerun", attributes, colour_scheme, used_task_types)

            else:
                get_dot_format_for_task_type(
                    "Task to run", attributes, colour_scheme, used_task_types)

            #
            #   graphviz attributes override other definitions
            #       presume the user knows what she is doing!
            #
            if(hasattr(n, 'graphviz_attributes')):
                for k in n.graphviz_attributes:
                    attributes[k] = n.graphviz_attributes[k]
            stream.write('t%d' % n._node_index +
                         attributes_to_str(attributes, _get_name(n)))

        else:
            #
            #   these jobs are up to date and will not be re-run
            #

            if not skip_uptodate_tasks:
                if n in target_jobs:
                    get_dot_format_for_task_type(
                        "Up-to-date Final target", attributes, colour_scheme, used_task_types)

                elif n in up_to_date_jobs:
                    get_dot_format_for_task_type(
                        "Up-to-date task", attributes, colour_scheme, used_task_types)

                #
                #   these jobs will be ignored: gray with gray dependencies
                #
                else:
                    get_dot_format_for_task_type(
                        "Down stream", attributes, colour_scheme, used_task_types)
                    delayed_task_strings.append(
                        't%d' % n._node_index + attributes_to_str(attributes, _get_name(n)))
                    for o in n._get_inward():
                        delayed_task_strings.append('t%d -> t%d[color=%s, arrowtype=normal];\n' % (
                            o._node_index, n._node_index, colour_scheme["Up-to-date"]["linecolor"]))
                    continue

            #
            #   graphviz attributes override other definitions
            #       presume the user knows what she is doing!
            #
            if(hasattr(n, 'graphviz_attributes')):
                for k in n.graphviz_attributes:
                    attributes[k] = n.graphviz_attributes[k]
            stream.write('t%d' % n._node_index +
                         attributes_to_str(attributes, _get_name(n)))

        #
        #   write edges
        #
        unconstrained = False
        for o in sorted(n._get_inward(), reverse=True, key=lambda x: x._node_index):
            #
            #   circularity violating DAG: highlight in red: should never be a constraint
            #       in drawing the graph
            #
            if (n, o) in dag_violating_dependencies:
                constraint_str = ", constraint=false" if o._node_index > n._node_index else ""
                vicious_cycle_task_strings.append('t%d -> t%d[color=%s %s];\n' % (
                    o._node_index, n._node_index, colour_scheme["Vicious cycle"]["linecolor"], constraint_str))
                continue
            elif not o in jobs_to_run or not n in jobs_to_run:
                if not skip_uptodate_tasks:
                    edge_str = 't%d -> t%d[color=%s, arrowtype=normal];\n' % (
                        o._node_index, n._node_index, colour_scheme["Up-to-date"]["linecolor"])
                    if unconstrained:
                        delayed_task_strings.append(edge_str)
                    else:
                        stream.write(edge_str)
            else:
                stream.write('t%d -> t%d[color=%s];\n' % (o._node_index,
                                                          n._node_index, colour_scheme["Task to run"]["linecolor"]))
            unconstrained = True

    for l in delayed_task_strings:
        stream.write(l)

    #
    #   write vicious cycle at end so not constraint in drawing graph
    #
    for l in vicious_cycle_task_strings:
        stream.write(l)
    stream.write('}\n')

    if not no_key_legend:
        write_legend_key(stream, used_task_types,
                         minimal_key_legend, colour_scheme)
    stream.write("}\n")

    ss = stream.getvalue().encode()
    byte_stream.write(ss)

    stream.close()
