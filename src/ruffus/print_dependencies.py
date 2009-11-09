#!/usr/bin/env python
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
"""
    print_dependencies.py
    
        provides support for dependency trees

"""

import types


#_________________________________________________________________________________________

#   Helper functions for dot format

#_________________________________________________________________________________________
def attributes_to_str (attributes, name):
    """
    helper function for dot format
    turns dictionary into a=b, c=d...
    """
    name = name.replace("__main__.", "")
    attributes["label"] = '"' + name + '"'

    return "[" + ", ".join ("%s=%s" % (k,v) for k,v in attributes.iteritems()) + "];\n"

def get_dot_format (task_type, attributes):
    if task_type == "Final target":
        attributes["fontcolor"]="orange"
        attributes["color"]="orange"
        attributes["shape"]="tripleoctagon"
    if task_type == "Up-to-date Final target":
        attributes["fontcolor"]="gray"
        attributes["color"]="gray"
        attributes["shape"]="tripleoctagon"
    if task_type == "Vicious cycle":
        attributes["fillcolor"]="red"
        attributes["shape"]="box"
        attributes["style"]="filled"
    elif task_type == "Task to run":
        attributes["fontcolor"]="blue"
        attributes["shape"]="plaintext"
    elif task_type == "Up-to-date task forced to rerun":
        attributes["fontcolor"]="blue"
        attributes["color"]="olivedrab"
        attributes["shape"]="tripleoctagon"
    elif task_type ==  "Force pipeline run from this task":
        attributes["fontcolor"]="blue"
        attributes["color"]="blue"
        attributes["shape"]="tripleoctagon"
    elif task_type == "Up-to-date task":
        attributes["color"] = "olivedrab"
        attributes["style"]="filled"
        attributes["fillcolor"]="olivedrab"
        attributes["fontcolor"]="black"
        attributes["shape"]="octagon"
    elif task_type == "Up-to-date dependence":
        attributes["color"] = "gray"
        attributes["style"]="filled"
        attributes["fillcolor"]="white"
        attributes["fontcolor"]="gray"
        attributes["shape"]="octagon"



def output_dependency_tree_key_in_dot_format (stream):
    """
    Write legend/key to dependency tree graph
    """
    stream.write( 'subgraph clusterkey\n')
    stream.write( '{\n')
    stream.write( 'style=filled;\n')
    stream.write( 'fontsize=30;\n')
    stream.write( 'color=gray90;\n')
    stream.write( 'label = "Key:";\n')
    stream.write( 'node[fontsize=10];\n')
    
    def outputkey (key_index, task_type, stream):
        attributes = dict()
        get_dot_format (task_type, attributes)
        attributes["fontsize"] = '15'
        stream.write('k%d' % key_index + attributes_to_str(attributes, task_type))

    for i, task_type in enumerate([ "Final target"                      ,
                                    "Vicious cycle"                     ,
                                    "Task to run"                       ,
                                    "Force pipeline run from this task" ,
                                    "Up-to-date Final target"           ,
                                    "Up-to-date task forced to rerun"   ,
                                    "Up-to-date task"                   ,
                                    "Up-to-date dependence" ]):
        outputkey(i + 1, task_type, stream)
        
            
    #
    #   white (invisible) lines between key to align
    # 
    stream.write(
                "k1->k2[color=red];"
                "k2->k1 [color=red];"
                "k2->k3->k4->k5[color=blue];"
                "k5->k6->k7->k8[color=gray];")
    stream.write("}\n")


#_________________________________________________________________________________________

#   output_dependency_tree_in_dot_format

#_________________________________________________________________________________________
def output_dependency_tree_in_dot_format(   jobs_to_run,
                                            up_to_date_jobs,
                                            dag_violating_edges, 
                                            dag_violating_nodes, 
                                            stream, 
                                            target_jobs, 
                                            forced_to_run_jobs = [], 
                                            all_jobs = None, vertical=True,
                                            skip_uptodate_tasks = False,
                                            no_key_legend             = False):
    """
        output_dependencies_in_dot_format

            jobs_to_run         = pipeline jobs which are not up to date or have dependencies
                                    which are not up to date
                                  Blue
            up_to_date_jobs     = Green       
            cyclic dependencies = Red (jobs and dependencies) 
            ignored jobs        = Gray
            target_jobs         = Orange
            forced_to_run_jobs  = Octagon
    """
    up_to_date_jobs  = set(up_to_date_jobs)

    # 
    #   cases where child points back to ancestor
    # 
    dag_violating_dependencies = set(dag_violating_edges)    
    


    stream.write( "digraph tree\n{\n")
    stream.write( 'size="8,11!";\n')
    stream.write( 'splines=true;\n')
    stream.write( 'fontsize=30;\n')
    stream.write( 'ranksep = 0.3;\n')
    if not vertical:
        stream.write( 'rankdir="LR";\n')
    stream.write( 'subgraph clustertasks\n'
                  "{\n")
    stream.write( 'label = "Pipeline:";\n')
    if vertical:
        stream.write( 'edge[minlen=2];\n')
    stream.write( 'node[fontsize=20];\n')
    delayed_task_strings = list()
    extra_delayed_task_strings = list()
    
    # 
    #   all jobs should be specified
    #       this is a bad fall-back
    #       because there is no guarantee that we are printing what we want to print
    if all_jobs == None:
        all_jobs = node.all_nodes
        
    for n in all_jobs:
        attributes = dict()
        #
        #   circularity violating DAG: highlight in red
        # 
        if n in dag_violating_nodes:
            get_dot_format ("Vicious cycle"                    , attributes)
            extra_delayed_task_strings.append('t%d' % n._node_index + attributes_to_str(attributes, n._name))
        #
        #   these jobs will be run
        # 
        elif n in jobs_to_run:

            # 
            #   up to date but forced to run: outlined in blue
            # 
            if n in forced_to_run_jobs:
                get_dot_format ("Force pipeline run from this task", attributes)

            #
            #   final target: outlined in orange 
            #
            elif n in target_jobs:
                get_dot_format("Final target"                  , attributes)
            
            # 
            #   up to date dependency but forced to run: outlined in green
            # 
            elif n in up_to_date_jobs:
                get_dot_format ("Up-to-date task forced to rerun"  , attributes)

            else:
                get_dot_format ("Task to run"                      , attributes)
            stream.write('t%d' % n._node_index + attributes_to_str(attributes, n._name))

        else:
            #
            #   these jobs are up to date and will not be re-run
            # 
            
            if not skip_uptodate_tasks:
                if n in target_jobs:
                    get_dot_format ("Up-to-date Final target"          , attributes)
                
                elif n in up_to_date_jobs:
                    get_dot_format ("Up-to-date task"                  , attributes)

                #
                #   these jobs will be ignored: gray with gray dependencies
                # 
                else:
                    get_dot_format ("Up-to-date dependence"            , attributes)
                    delayed_task_strings.append('t%d' % n._node_index + attributes_to_str(attributes, n._name))
                    for o in n.outward():
                        delayed_task_strings.append('t%d -> t%d[color=gray, arrowtype=normal];\n' % (o._node_index, n._node_index))
                    continue

            stream.write('t%d' % n._node_index + attributes_to_str(attributes, n._name))

        # 
        #   write edges
        # 
        unconstrained = False
        for o in sorted(n.outward(), reverse=True, key = lambda x: x._node_index):
            #
            #   circularity violating DAG: highlight in red: should never be a constraint
            #       in drawing the graph
            # 
            if (n, o) in dag_violating_dependencies:
                constraint_str = ", constraint=false" if o._node_index >  n._node_index else ""
                extra_delayed_task_strings.append('t%d -> t%d[color=red %s];\n' % (o._node_index, n._node_index, constraint_str))
                continue
            elif not o in jobs_to_run or not n in jobs_to_run:
                if not skip_uptodate_tasks:
                    edge_str = 't%d -> t%d[color=gray, arrowtype=normal];\n' % (o._node_index, n._node_index)
                    if unconstrained:
                        delayed_task_strings.append(edge_str)
                    else:
                        stream.write(edge_str)
            else:
                stream.write('t%d -> t%d[color=blue];\n' % (o._node_index, n._node_index))
            unconstrained = True

    for l in delayed_task_strings:
        stream.write(l)
    for l in extra_delayed_task_strings:
        stream.write(l)
    stream.write( '}\n')

        
    if not no_key_legend:
        output_dependency_tree_key_in_dot_format (stream)
    stream.write("}\n")


