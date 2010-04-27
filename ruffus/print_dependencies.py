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
from adjacent_pairs_iterate import adjacent_pairs_iterate


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

    
def get_connection_dot_str (from_task_type, to_task_type, n1, n2):
    if "Vicious cycle" in (from_task_type, to_task_type):
        return ("%s -> %s[color=red, arrowtype=normal];\n" % (n1, n2) +
                "%s -> %s[color=red, arrowtype=normal];\n" % (n2, n1))
    if from_task_type in ("Final target", "Task to run",
                            "Up-to-date task forced to rerun",
                            "Force pipeline run from this task"):
        return "%s -> %s[color=blue, arrowtype=normal];\n" % (n1, n2)
    elif from_task_type in ("Up-to-date task", "Up-to-date dependence","Up-to-date Final target"):
        return "%s -> %s[color=gray, arrowtype=normal];\n" % (n1, n2)
    # 
    # shouldn't be here!!
    # 
    else:
        return "%s -> %s[color=gray, arrowtype=normal];\n" % (n1, n2)

def get_dot_format (task_type, attributes, used_formats):
    used_formats.add(task_type)
    if task_type == "Final target":
        attributes["fontcolor"]="orange"
        attributes["color"]="orange"
        attributes["peripheries"] = 2
    elif task_type == "Up-to-date Final target":
        attributes["fontcolor"]="gray"
        attributes["color"]="gray"
        attributes["peripheries"] = 2
    elif task_type == "Vicious cycle":
        attributes["fillcolor"]="red"
        attributes["color"]="red"
        #attributes["shape"]="box"
        attributes["style"]="filled"
    elif task_type == "Task to run":
        attributes["fontcolor"]="blue"
        #attributes["shape"]="plaintext"
        attributes["color"]="blue"
    elif task_type == "Up-to-date task forced to rerun":
        attributes["fontcolor"]="blue"
        #attributes["color"]="olivedrab"
        attributes["color"]="blue"
        attributes["style"]="dashed"
        #attributes["shape"]="tripleoctagon"
        #attributes["peripheries"] = 2
    elif task_type ==  "Force pipeline run from this task":
        attributes["fontcolor"]="blue"
        attributes["color"]="blue"
        #attributes["shape"]="tripleoctagon"
        attributes["peripheries"] = 2
    elif task_type == "Up-to-date task":
        attributes["color"] = "olivedrab"
        attributes["style"]="filled"
        attributes["fillcolor"]="olivedrab"
        attributes["fontcolor"]="black"
        #attributes["shape"]="octagon"
    elif task_type == "Up-to-date dependence":
        attributes["color"] = "gray"
        attributes["style"]="filled"
        attributes["fillcolor"]="white"
        attributes["fontcolor"]="gray"
        #attributes["shape"]="octagon"



def output_dependency_tree_key_in_dot_format (stream, used_task_types, minimal_key_legend):
    """
    Write legend/key to dependency tree graph
    """
    if not len(used_task_types):
        return
        

    stream.write( 'subgraph clusterkey\n')
    stream.write( '{\n')
    stream.write( 'style=filled;\n')
    #stream.write( 'fontsize=30;\n')
    stream.write( 'color=gray90;\n')
    stream.write( 'label = "Key:";\n')
    stream.write( 'node[margin=0.2,0.2];\n')
    
        
    #
    #   Only include used task types
    # 
    all_task_types = [ 
                       "Vicious cycle"                     ,
                       "Up-to-date dependence" ,
                       "Up-to-date task"                   ,
                       "Force pipeline run from this task" ,
                       "Task to run"                       ,
                       "Up-to-date task forced to rerun"   ,
                       "Up-to-date Final target"           ,
                       "Final target"                      ,]
    if not minimal_key_legend:
        used_task_types |= set(all_task_types)
    wrapped_task_types = [ 
                       "Vicious cycle"                     ,
                       "Up-to-date\\ndependence" ,
                       "Up-to-date task"                   ,
                       "Force pipeline run\\nfrom this task" ,
                       "Task to run"                       ,
                       "Up-to-date task\\nforced to rerun"   ,
                       "Up-to-date\\nFinal target"           ,
                       "Final target"                      ,]
    wrapped_task_types = dict(zip(all_task_types, wrapped_task_types))


    def outputkey (key, task_type, stream):
        ignore_used_task_types = set()
        attributes = dict()
        attributes["shape"] = "rect"
        get_dot_format (task_type, attributes, ignore_used_task_types)
        #attributes["fontsize"] = '15'
        stream.write(key + attributes_to_str(attributes, wrapped_task_types[task_type]))


    sorted_used_task_types = []
    for t in all_task_types:
        if t in used_task_types:
            sorted_used_task_types.append(t)
    
    # print first key type
    outputkey("k1", sorted_used_task_types[0], stream)

    for i, (from_task_type, to_task_type) in enumerate(adjacent_pairs_iterate(sorted_used_task_types)):
        from_key = 'k%d' % (i + 1)
        to_key = 'k%d' % (i + 2)
        # write key
        outputkey(to_key, to_task_type, stream)
        # connection between keys
        stream.write(get_connection_dot_str (from_task_type, to_task_type, from_key, to_key))
        
            
    #stream.write(
    #            "k1->k2[color=red];"
    #            "k2->k1 [color=red];"
    #            "k2->k3->k4->k5[color=blue];"
    #            "k5->k6->k7->k8[color=gray];")
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
                                            forced_to_run_jobs      = [], 
                                            all_jobs                = None, 
                                            vertical                = True,
                                            skip_uptodate_tasks     = False,
                                            no_key_legend           = False,
                                            minimal_key_legend      = True):
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
    stream.write( 'node[fontsize=20];\n')
    #stream.write( 'node[regular=1];\n')
    if not vertical:
        stream.write( 'rankdir="LR";\n')
    stream.write( 'subgraph clustertasks\n'
                  "{\n")
    stream.write( 'label = "Pipeline:";\n')
    #if vertical:
    #    stream.write( 'edge[minlen=2];\n')
    delayed_task_strings = list()
    vicious_cycle_task_strings = list()
    
    # 
    #   all jobs should be specified
    #       this is a bad fall-back
    #       because there is no guarantee that we are printing what we want to print
    if all_jobs == None:
        all_jobs = node.all_nodes
        
        
    used_task_types = set()
    
    #
    #   defined duplicately in graph. Bad practice
    #     
    one_to_one              = 0 
    many_to_many            = 1 
    one_to_many             = 2 
    many_to_one             = 3 
        
    for n in all_jobs:
        attributes = dict()
        attributes["shape"] = "rect"
        if hasattr(n, "single_multi_io"):
            if n.single_multi_io == one_to_many:
                attributes["shape"] = "house"
            elif n.single_multi_io == many_to_one:
                attributes["shape"] = "invhouse"
                attributes["height"] = 1.1
            
                
        #
        #   circularity violating DAG: highlight in red
        # 
        if n in dag_violating_nodes:
            get_dot_format ("Vicious cycle"                    , attributes, used_task_types)
            vicious_cycle_task_strings.append('t%d' % n._node_index + attributes_to_str(attributes, n._name))
        #
        #   these jobs will be run
        # 
        elif n in jobs_to_run:

            # 
            #   up to date but forced to run: outlined in blue
            # 
            if n in forced_to_run_jobs:
                get_dot_format ("Force pipeline run from this task", attributes, used_task_types)

            #
            #   final target: outlined in orange 
            #
            elif n in target_jobs:
                get_dot_format("Final target"                  , attributes, used_task_types)
            
            # 
            #   up to date dependency but forced to run: outlined in green
            # 
            elif n in up_to_date_jobs:
                get_dot_format ("Up-to-date task forced to rerun"  , attributes, used_task_types)

            else:
                get_dot_format ("Task to run"                      , attributes, used_task_types)
            stream.write('t%d' % n._node_index + attributes_to_str(attributes, n._name))

        else:
            #
            #   these jobs are up to date and will not be re-run
            # 
            
            if not skip_uptodate_tasks:
                if n in target_jobs:
                    get_dot_format ("Up-to-date Final target"          , attributes, used_task_types)
                
                elif n in up_to_date_jobs:
                    get_dot_format ("Up-to-date task"                  , attributes, used_task_types)

                #
                #   these jobs will be ignored: gray with gray dependencies
                # 
                else:
                    get_dot_format ("Up-to-date dependence"            , attributes, used_task_types)
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
                vicious_cycle_task_strings.append('t%d -> t%d[color=red %s];\n' % (o._node_index, n._node_index, constraint_str))
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
        
    #
    #   write vicious cycle at end so not constraint in drawing graph
    # 
    for l in vicious_cycle_task_strings:
        stream.write(l)
    stream.write( '}\n')

        
    if not no_key_legend:
        output_dependency_tree_key_in_dot_format (stream, used_task_types, minimal_key_legend)
    stream.write("}\n")


