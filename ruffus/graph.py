from __future__ import print_function
################################################################################
#
#   graph.py
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
    graph.py

        provides support for diacyclic graph
        with topological_sort

"""
import sys
import re
import os

# use simplejson in place of json for python < 2.6
try:
    import json
except ImportError:
    import simplejson
    json = simplejson

from collections import defaultdict
from .print_dependencies import *
import tempfile
import subprocess
# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   class node

# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888


class graph_error(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class error_duplicate_node_name(graph_error):
    pass


class node (object):
    """
    node
        designed for diacyclic graphs but can hold anything
        contains lists of nodes and
        dictionary to look up node name from node
    """

    _all_nodes = list()
    _name_to_node = dict()
    _index_to_node = dict()
    _global_node_index = 0

    _one_to_one = 0
    _many_to_many = 1
    _one_to_many = 2
    _many_to_one = 3

    @staticmethod
    def _get_leaves():
        for n in node._all_nodes:
            if len(n._inward) == 0:
                yield n

    @staticmethod
    def _get_roots():
        for n in node._all_nodes:
            if len(n._outward) == 0:
                yield n

    @staticmethod
    def _count_nodes():
        return len(_all_nodes)

    @staticmethod
    def _dump_tree_as_str():
        """
        dumps entire tree
        """
        return ("%d nodes " % node._count_nodes()) + "\n" + \
            "\n".join([x._fullstr() for x in node._all_nodes])

    @staticmethod
    def _lookup_node_from_name(name):
        return node._name_to_node[name]

    @staticmethod
    def _lookup_node_from_index(index):
        return node._index_to_node[index]

    @staticmethod
    def _is_node(name):
        return name in node._name_to_node

    # _____________________________________________________________________________________

    #   init

    # _____________________________________________________________________________________

    def __init__(self, name, **args):
        """
        each node has
            _name
            _inward :   lists of incoming edges
            _outward:   lists of outgoing edges
        """
        #
        #   make sure node name is unique
        #
        # if name in node._name_to_node:
        #    raise error_duplicate_node_name("[%s] has already been added" % name)

        self.__dict__.update(args)
        self._inward = list()
        self._outward = list()
        self.args = args
        self._name = name
        self._signal = False
        self._node_index = node._global_node_index
        node._global_node_index += 1

        #
        #   for looking up node for name
        #
        node._all_nodes.append(self)
        node._name_to_node[self._name] = self
        node._index_to_node[self._node_index] = self

    # _____________________________________________________________________________________

    #   _add_child

    # _____________________________________________________________________________________
    def _add_child(self, child):
        """
        connect edges
        """
        # do not add duplicates
        if child in self._outward:
            return child

        self._outward.append(child)
        child._inward.append(self)
        return child

    # _____________________________________________________________________________________

    #   _remove_child

    # _____________________________________________________________________________________
    def _remove_child(self, child):
        """
        disconnect edges
        """

        if child in self._outward:
            self._outward.remove(child)
        if self in child._inward:
            child._inward.remove(self)
        return child
    # _____________________________________________________________________________________

    #   _add_parent

    # _____________________________________________________________________________________
    def _add_parent(self, parent):
        """
        connect edges
        """
        # do not add duplicates
        if parent in self._inward:
            return parent

        self._inward.append(parent)
        parent._outward.append(self)
        return parent

    # _____________________________________________________________________________________

    #   _remove_all_parents

    # _____________________________________________________________________________________
    def _remove_all_parents(self):
        """
        disconnect edges
        """

        # remove self from parent
        for parent in self._inward:
            if self in parent._outward:
                parent._outward.remove(self)

        # clear self
        self._inward = []

        return self

    # _____________________________________________________________________________________

    #   _remove_parent

    # _____________________________________________________________________________________
    def _remove_parent(self, parent):
        """
        disconnect edges
        """

        if parent in self._inward:
            self._inward.remove(parent)
        if self in parent._outward:
            parent._outward.remove(self)
        return parent
    # _____________________________________________________________________________________

    #   _get_inward/_get_outward

    # _____________________________________________________________________________________
    def _get_outward(self):
        """
        just in case we need to return inward when we mean outward!
            (for reversed graphs)
        """
        return self._outward

    def _get_inward(self):
        """
        just in case we need to return inward when we mean outward!
            (for reversed graphs)
        """
        return self._inward

    # _____________________________________________________________________________________

    #   _fullstr

    # _____________________________________________________________________________________

    def _fullstr(self):
        """
        Full dump. Normally edges are not printed out
        Everything is indented except name
        """
        self_desc = list()
        for k, v in sorted(iter(self.__dict__.items()), key=lambda x_v: (0, x_v[0], x_v[1]) if x_v[0] == "_name" else (1, x_v[0], x_v[1])):
            indent = "    " if k != "_name" else ""
            if k in ("_inward", "_outward"):
                v = ",".join([x._name for x in v])
                self_desc.append(indent + str(k) + "=" + str(v))
            else:
                self_desc.append(indent + str(k) + "=" + str(v))
        return "\n".join(self_desc)

    # _____________________________________________________________________________________

    #   __str__

    # _____________________________________________________________________________________
    def __str__(self):
        """
        Print everything except lists of edges
        Useful for debugging
        """
        self_desc = list()
        for k, v in sorted(self.__dict__.items(), reverse=True):
            indent = "    " if k != "_name" else ""
            if k[0] == '_':
                continue
            else:
                self_desc.append(indent + str(k) + "=" + str(v))
        return "  Task = " + "\n".join(self_desc)

    # _____________________________________________________________________________________

    #   _signalled
    #
    # _____________________________________________________________________________________

    def _signalled(self, extra_data_for_signal=None):
        """
        Signals whether depth first search ends without this node
        """
        return self._signal


# _____________________________________________________________________________________

#   node_to_json
#
#
# _____________________________________________________________________________________
class node_to_json(json.JSONEncoder):
    """
    output node using json
    """

    def default(self, obj):
        print(str(obj))
        if isinstance(obj, node):
            return obj._name, {
                "index": obj._node_index,
                "_signal": obj._signal,
                "_get_inward": [n._name for n in obj._inward],
                "_get_outward": [n._name for n in obj._outward],
            }
        return json.JSONEncoder.default(self, obj)


# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   topological_sort_visitor

# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888


def default_signalled(node, extra_data):
    """
    Depth first search stops when node._signalled return True
    """
    return node._signalled(extra_data)


class topological_sort_visitor (object):
    """
    topological sort
        used with DFS to find all nodes in topologically sorted order
        All finds all DAG breaking cycles

    """

    IGNORE_NODE_SIGNAL = 0
    NOTE_NODE_SIGNAL = 1
    END_ON_SIGNAL = 2

    # _____________________________________________________________________________________

    #   init

    # _____________________________________________________________________________________
    def __init__(self, forced_dfs_nodes,
                 node_termination=END_ON_SIGNAL,
                 extra_data_for_signal=None,
                 signal_callback=None):
        """
        list of saved results
        """
        self._forced_dfs_nodes = set(forced_dfs_nodes)
        self._node_termination = node_termination

        self._start_nodes = set()
        self._back_edges = set()
        self._back_nodes = set()
        self._signalling_nodes = set()

        self.signal_callback = signal_callback

        # keep order for tree traversal later
        self._examined_edges = list()
        # keep order for topological sorted results
        self._finished_nodes = list()

        self._extra_data_for_signal = extra_data_for_signal

    def combine_with(self, other):
        """
        combine the results of two visitors
            (add other to self)
        """
        self._back_edges              .update(other._back_edges)
        self._back_nodes              .update(other._back_nodes)
        extra_finished_nodes = set(
            other._finished_nodes) - set(self._finished_nodes)
        self._finished_nodes          .extend(extra_finished_nodes)

    # _____________________________________________________________________________________

    #   __str__

    # _____________________________________________________________________________________

    def __str__(self):
        """
        for diagnostics
        """
        signalling_str = get_nodes_str("Signalling", self._signalling_nodes)
        finished_str = get_nodes_str("Finished", self._finished_nodes)
        forced_str = get_nodes_str("Forced to run", self._forced_dfs_nodes)
        start_str = get_nodes_str("Start", self._start_nodes)
        back_edges_str = get_edges_str("back", self._back_edges)
        return (""
                + finished_str
                + start_str
                + back_edges_str
                + signalling_str
                + finished_str
                )

    # _____________________________________________________________________________________

    #   not_dag

    # _____________________________________________________________________________________
    def not_dag(self):
        """
        back edges add circularity
        """
        return len(self._back_edges)

    # _____________________________________________________________________________________

    #   dag_violating_edges

    # _____________________________________________________________________________________
    def dag_violating_edges(self):
        """
        back edges add circularity
        """
        return self._back_edges

    # _____________________________________________________________________________________

    #   dag_violating_nodes

    # _____________________________________________________________________________________

    def dag_violating_nodes(self):
        """
        all nodes involved in cycless
        """
        return self._back_nodes

    # _____________________________________________________________________________________

    #   identify_dag_violating_nodes_and_edges
    #
    # _____________________________________________________________________________________
    def identify_dag_violating_nodes_and_edges(self):
        """
        find all nodes and edges in any cycles

        All dag violating cycles are defined by the back edge identified in DFS.
        All paths which go the other way: start at the to_node and end up at the from_node
            are therefore also part of the cycle

        """
        if not len(self._back_edges):
            return
        cnt_examined_edges = len(self._examined_edges)

        # add this to _back_edges at the end
        cycle_edges = set()

        #
        #   each cycle
        #       starts from the to_node   of each back_edge and
        #       ends   with the from_node of each back_edge
        #
        for cycle_to_node, cycle_from_node in self._back_edges:
            start_search_from = 0
            while 1:
                #
                # find start of cycle
                for i, (f, t, n) in enumerate(self._examined_edges[start_search_from:]):
                    if f == cycle_from_node:
                        break

                # no more cycles for this cycle_from_node/cycle_to_node pair
                else:
                    break

                #
                # cycle end might be within the same pair
                #   if so, don't search the current (not the next) edge for the cycle end
                #
                #   Otherwise incrementing search position avoids infinite loop
                #
                start_search_from = cycle_start = start_search_from + i
                if self._examined_edges[cycle_start][1] != cycle_to_node:
                    start_search_from += 1

                for i, (f, t, n) in enumerate(self._examined_edges[start_search_from:]):

                    #
                    #   found end of cycle
                    #
                    if t == cycle_to_node:
                        cycle_end = start_search_from + i + 1
                        #
                        #   ignore backtracked nodes which will not be part of the cycle
                        #       we are essentially doing tree traversal here
                        #
                        backtracked_nodes = set()
                        for f, t, n in self._examined_edges[cycle_start:cycle_end]:
                            if t is None:
                                backtracked_nodes.add(n)
                        for f, t, n in self._examined_edges[cycle_start:cycle_end]:
                            if f is None or f in backtracked_nodes or t in backtracked_nodes:
                                continue
                            cycle_edges.add((f, t))
                            self._back_nodes.add(f)
                            self._back_nodes.add(t)
                        start_search_from = cycle_end
                        break

                    # if cycle_from_node comes around again, this is not a cycle
                    if cycle_from_node == f:
                        if not i:
                            i += 1
                        start_search_from = start_search_from + i
                        break

                    continue

                # no more cycles for this cycle_from_node/cycle_to_node pair
                else:
                    break

        self._back_edges.update(cycle_edges)

    # _____________________________________________________________________________________

    #   not_dag

    # _____________________________________________________________________________________

    def topological_sorted(self):
        """
        _finished_nodes
        """
        return self._finished_nodes

    # _____________________________________________________________________________________

    #   terminate_before

    # _____________________________________________________________________________________

    def terminate_before(self, node):
        """
        Allow node to terminate this path in DFS without including itself
            (see terminate_at)

        If node in _forced_dfs_nodes that overrides what the node wants
        """

        #
        #   If _node_termination = IGNORE_NODE_TERMINATION
        #       always go through whole tree
        #
        if self._node_termination == self.IGNORE_NODE_SIGNAL:
            return False

        #
        #   If _node_termination = NOTE_NODE_TERMINATION
        #       always go through whole tree but remember
        #       which nodes want to terminate
        #
        #   Note that _forced_dfs_nodes is ignored
        #
        if self._node_termination == self.NOTE_NODE_SIGNAL:
            if self.signal_callback(node, self._extra_data_for_signal):
                self._signalling_nodes.add(node)
            return False

        #
        #   _forced_dfs_nodes always overrides node preferences
        #       but let us save what the node says anyway for posterity
        #
        if node in self._forced_dfs_nodes:
            # Commented out code lets us save self_terminating_nodes even when
            # they have been overridden by _forced_dfs_nodes
            # if self.signal_callback(node, self._extra_data_for_signal):
            #    self._signalling_nodes.add(node)
            return False

        #
        #   OK. Go by what the node wants then
        #
        if self.signal_callback(node, self._extra_data_for_signal):
            self._signalling_nodes.add(node)
            return True
        return False

    # _____________________________________________________________________________________

    #   call_backs

    # _____________________________________________________________________________________

    def discover_vertex(self, node):
        pass

    def start_vertex(self, node):
        self._start_nodes.add(node)

    def finish_vertex(self, node):
        """
        Save
            1) topologically sorted nodes
            2) as "None" (back) edges which allows _examined_edges to be traversed
               like a tree

        """
        self._examined_edges.append((None, None, node))
        self._finished_nodes.append(node)

    def examine_edge(self, node_from, node_to):
        """
        Save edges as we encounter then so we can look for loops

        """
        self._examined_edges.append((node_from, node_to, None))

    def back_edge(self, node_from, node_to):
        self._back_edges.add((node_from, node_to))

    def tree_edge(self, node_from, node_to):
        pass

    def forward_or_cross_edge(self, node_from, node_to):
        pass

    def terminate_at(self, node):
        """
        Terminate this line of DFS but include myself
        """
        return False

#
# _________________________________________________________________________________________

#   debug_print_visitor

# _________________________________________________________________________________________


class debug_print_visitor (object):
    """
    log progress through DFS: for debugging

    """

    def terminate_before(self, node):
        return False

    def terminate_at(self, node):
        return False

    def start_vertex(self, node):
        print("s  start vertex %s" % (node._name))

    def finish_vertex(self, node):
        print("  v  finish vertex %s" % (node._name))

    def discover_vertex(self, node):
        print("  |  discover vertex %s" % (node._name))

    def examine_edge(self, node_from, node_to):
        print("  -- examine edge %s -> %s" % (node_from._name, node_to._name))

    def back_edge(self, node_from, node_to):
        print("    back edge %s -> %s" % (node_from._name, node_to._name))

    def tree_edge(self, node_from, node_to):
        print("   - tree edge %s -> %s" % (node_from._name, node_to._name))

    def forward_or_cross_edge(self, node_from, node_to):
        print("   - forward/cross edge %s -> %s" %
              (node_from._name, node_to._name))


# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888
#   Functions
# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888
# _________________________________________________________________________________________
#   depth first search
# _________________________________________________________________________________________
#
#
#
WHITE = 0       # virgin
GRAY = 1       # processing
BLACK = 2       # finished


def depth_first_visit(u, visitor, colours, outedges_func):
    """
    depth_first_visit
        unused callbacks are commented out
    """
    # start processing this node: so gray
    colours[u] = GRAY

    stack = list()

    #
    # unused callback
    #
    # visitor.discover_vertex(u)

    curr_edges = outedges_func(u)

    if visitor.terminate_before(u):
        colours[u] = BLACK
        return
    # If this vertex terminates the search, we push empty range
    if visitor.terminate_at(u):
        stack.append((u, curr_edges, len(curr_edges)))
    else:
        stack.append((u, curr_edges, 0))

    while len(stack):
        u, curr_edges, curr_edge_pos = stack.pop()
        while curr_edge_pos < len(curr_edges):
            v = curr_edges[curr_edge_pos]
            visitor.examine_edge(u, v)
            v_colour = colours[v]

            if visitor.terminate_before(v):
                colours[v] = BLACK
                curr_edge_pos += 1
                continue

            if v_colour == WHITE:
                #
                # unused callback
                #
                #visitor.tree_edge(u, v)
                curr_edge_pos += 1
                stack.append((u, curr_edges, curr_edge_pos))
                u = v
                colours[u] = GRAY
                #
                # unused callback
                #
                # visitor.discover_vertex(u)
                curr_edges = outedges_func(u)
                curr_edge_pos = 0

                if visitor.terminate_at(u):
                    break
            elif v_colour == GRAY:
                visitor.back_edge(u, v)
                curr_edge_pos += 1
            else:
                #
                # unused callback
                #
                #visitor.forward_or_cross_edge(u, v)
                curr_edge_pos += 1
        colours[u] = BLACK
        visitor.finish_vertex(u)


def depth_first_search(starting_nodes, visitor, outedges_func=node._get_inward):
    """
    depth_first_search
        go through all starting points and DFV on each of them
        if they haven't been seen before
    """
    colours = defaultdict(int)  # defaults to WHITE
    if len(starting_nodes):
        for start in starting_nodes:
            if colours[start] == WHITE:
                visitor.start_vertex(start)
                depth_first_visit(start, visitor, colours, outedges_func)
    else:

        #
        #   go through all nodes, maintaining order
        #
        for start in node._all_nodes:
            if colours[start] == WHITE:
                visitor.start_vertex(start)
                depth_first_visit(start, visitor, colours, outedges_func)


def topologically_sorted_nodes(to_leaves,
                               force_start_from=[],
                               gather_all_non_signalled=True,
                               test_all_signals=False,
                               extra_data_for_signal=None,
                               signal_callback=None):
    """
    Get all nodes which are children of to_leaves
        in topological sorted order

    Defaults to including all nodes which are non-signalled and their dependents (via include_any_children())
        i.e. includes the *last* non-signalling node on each branch and all the way up the tree


    Otherwise stops at each branch just before signalling node
        i.e. includes the last non-signalling *run* on each branch


    force_start_from
    Optionally specify all the child nodes which *have* to
        be included in the list at least
        This will override any node signals

    force_start_from = True to get the whole tree irrespective of signalling


    Rewritten to minimise calls to node._signalled()

    """

    #
    #   got through entire tree, looking for signalling nodes,
    #       usually for debugging or for printing
    #
    if test_all_signals:
        v = topological_sort_visitor([],
                                     topological_sort_visitor.NOTE_NODE_SIGNAL,
                                     extra_data_for_signal,
                                     signal_callback)
        depth_first_search(to_leaves, v, node._get_inward)
        signalling_nodes = v._signalling_nodes
    else:
        signalling_nodes = set()

    if gather_all_non_signalled:
        #
        #   get whole tree, ignoring signalling
        #
        v = topological_sort_visitor(
            [], topological_sort_visitor.IGNORE_NODE_SIGNAL)
        depth_first_search(to_leaves, v, node._get_inward)

        #
        #   not dag: no further processing
        #
        if v.not_dag():
            v.identify_dag_violating_nodes_and_edges()
            return (v.topological_sorted(), v._signalling_nodes, v.dag_violating_edges(),
                    v.dag_violating_nodes())

        #
        #   if force_start_from == True
        #
        #       return entire tree
        #
        if force_start_from == True:
            return (v.topological_sorted(), v._signalling_nodes, v.dag_violating_edges(),
                    v.dag_violating_nodes())

        #
        #   Set of all nodes we are going to return
        #   We will use v.topological_sorted to return them in the right (sorted) order
        #
        nodes_to_include = set()

        #
        #   If force start from is a list of nodes,
        #       include these and all of its dependents (via include_any_children)
        #
        #   We don't need to bother to check if they signal (_signalled)
        #   This saves calling the expensive _signalled
        #
        if len(force_start_from):
            nodes_to_include.update(include_any_children(force_start_from))
        # This should not be necessary because include_any_children also returns self.
        # for n in force_start_from:
        #    if n in nodes_to_include:
        #        continue
        #    nodes_to_include.add(n)
        #    nodes_to_include.update(include_any_children([n]))

        #
        #   Now select all nodes from ancestor -> descendant which do not signal (signal_callback() == false)
        #       and select their descendants (via include_any_children())
        #
        #   Nodes which signal are added to signalling_nodes
        #
        reversed_nodes = v.topological_sorted()
        for n in reversed_nodes:
            if n in nodes_to_include:
                continue

            if not signal_callback(n, extra_data_for_signal):
                # nodes_to_include.add(n)
                nodes_to_include.update(include_any_children([n]))
            else:
                signalling_nodes.add(n)
                #sys.stderr.write(json.dumps(n, cls=node_to_json, sort_keys=1) + "\n")

        return ([n for n in v.topological_sorted() if n in nodes_to_include],
                signalling_nodes,
                [], [])

    #
    #   gather_all_non_signalled = False
    #       stop at first signalled
    #
    else:

        if force_start_from == True:
            #
            #   get whole tree, ignoring signalling
            #
            v = topological_sort_visitor([],
                                         topological_sort_visitor.IGNORE_NODE_SIGNAL)
        else:
            #
            #   End at each branch without including signalling node
            #       but ignore signalling for forced_nodes_and_dependencies
            #

            #   Get forced nodes and all descendants via include_any_children
            #
            forced_nodes_and_dependencies = []
            if len(force_start_from):
                forced_nodes_and_dependencies = include_any_children(
                    force_start_from)

            v = topological_sort_visitor(forced_nodes_and_dependencies,
                                         topological_sort_visitor.END_ON_SIGNAL,
                                         extra_data_for_signal,
                                         signal_callback)

        #
        #   Forward graph iteration
        #
        depth_first_search(to_leaves, v, node._get_inward)

        if v.not_dag():
            v.identify_dag_violating_nodes_and_edges()

        signalling_nodes.update(v._signalling_nodes)
        return (v.topological_sorted(), signalling_nodes, v.dag_violating_edges(), v.dag_violating_nodes())


#
def debug_print_nodes(to_leaves):
    v = debug_print_visitor()
    depth_first_search(to_leaves, v, node._get_inward)


# _________________________________________________________________________________________

#   graph_printout

# _________________________________________________________________________________________
def graph_colour_demo_printout(stream,
                               output_format,
                               size='11,8',
                               dpi='120'):
    """
    Demo of the different colour schemes
    """

    if output_format == 'dot':
        write_colour_scheme_demo_in_dot_format(stream)
        return

    # print to dot file
    #temp_dot_file = tempfile.NamedTemporaryFile(suffix='.dot', delete=False)
    fh, temp_dot_file_name = tempfile.mkstemp(suffix='.dot')
    temp_dot_file = os.fdopen(fh, "w")

    write_colour_scheme_demo_in_dot_format(temp_dot_file)
    temp_dot_file.close()

    print_dpi = ("-Gdpi='%s'" % dpi) if output_format != "svg" else ""
    run_dot = os.popen("dot -Gsize='%s' %s -T%s < %s" %
                       (size, print_dpi, output_format, temp_dot_file_name))

    #
    #   wierd bug fix for firefox and svg
    #
    result_str = run_dot.read()
    err = run_dot.close()
    if err:
        raise RuntimeError("dot failed to run with exit code %d" % err)
    if output_format == "svg":
        result_str = result_str.replace("0.12", "0.0px")
    stream.write(result_str)
# _________________________________________________________________________________________

#   graph_printout_in_dot_format

# _________________________________________________________________________________________


def graph_printout_in_dot_format(stream,
                                 to_leaves,
                                 force_start_from=[],
                                 draw_vertically=True,
                                 ignore_upstream_of_target=False,
                                 skip_signalling_nodes=False,
                                 gather_all_non_signalled=True,
                                 test_all_signals=True,
                                 no_key_legend=False,
                                 minimal_key_legend=True,
                                 user_colour_scheme=None,
                                 pipeline_name="Pipeline:",
                                 extra_data_for_signal=None,
                                 signal_callback=None):
    """
    print out pipeline dependencies in dot formatting
    """

    (topological_sorted,        # tasks_to_run
     signalling_nodes,           # up to date
     dag_violating_edges,
     dag_violating_nodes) = topologically_sorted_nodes(to_leaves, force_start_from,
                                                       gather_all_non_signalled,
                                                       test_all_signals,
                                                       extra_data_for_signal,
                                                       signal_callback)

    #
    #   N.B. For graph:
    #           upstream   = parent
    #           dependents/downstream
    #                      = children
    #
    #
    nodes_to_display = get_reachable_nodes(
        to_leaves, not ignore_upstream_of_target)

    #
    #   print out dependencies in dot format
    #
    write_flowchart_in_dot_format(topological_sorted,           # tasks_to_run
                                  signalling_nodes,             # up to date
                                  dag_violating_edges,
                                  dag_violating_nodes,
                                  stream,
                                  to_leaves,
                                  force_start_from,
                                  nodes_to_display,
                                  draw_vertically,
                                  skip_signalling_nodes,
                                  no_key_legend,
                                  minimal_key_legend,
                                  user_colour_scheme,
                                  pipeline_name)

# _________________________________________________________________________________________

#   graph_printout

# _________________________________________________________________________________________


def graph_printout(stream,
                   output_format,
                   to_leaves,
                   force_start_from=[],
                   draw_vertically=True,
                   ignore_upstream_of_target=False,
                   skip_signalling_nodes=False,
                   gather_all_non_signalled=True,
                   test_all_signals=True,
                   no_key_legend=False,
                   minimal_key_legend=True,
                   user_colour_scheme=None,
                   pipeline_name="Pipeline:",
                   size=(11, 8),
                   dpi=120,
                   extra_data_for_signal=None,
                   signal_callback=None):
    """
    print out pipeline dependencies in a variety of formats, using the programme "dot"
        an intermediary
    """

    if output_format == 'dot':
        graph_printout_in_dot_format(stream,
                                     to_leaves,
                                     force_start_from,
                                     draw_vertically,
                                     ignore_upstream_of_target,
                                     skip_signalling_nodes,
                                     gather_all_non_signalled,
                                     test_all_signals,
                                     no_key_legend,
                                     minimal_key_legend,
                                     user_colour_scheme,
                                     pipeline_name,
                                     extra_data_for_signal,
                                     signal_callback)
        return

    # print to dot file
    #temp_dot_file = tempfile.NamedTemporaryFile(suffix='.dot', delete=False)
    fh, temp_dot_file_name = tempfile.mkstemp(suffix='.dot')
    temp_dot_file = os.fdopen(fh, "wb")

    graph_printout_in_dot_format(temp_dot_file,
                                 to_leaves,
                                 force_start_from,
                                 draw_vertically,
                                 ignore_upstream_of_target,
                                 skip_signalling_nodes,
                                 gather_all_non_signalled,
                                 test_all_signals,
                                 no_key_legend,
                                 minimal_key_legend,
                                 user_colour_scheme,
                                 pipeline_name,
                                 extra_data_for_signal,
                                 signal_callback)
    temp_dot_file.close()

    if isinstance(size, tuple):
        print_size = "(%d,%d)" % size
    elif isinstance(size, (str)):
        print_size = size
    else:
        raise Exception(
            "Flowchart print size [%s] should be specified as a tuple of X,Y in inches" % str(size))

    #
    #   N.B. Resolution doesn't seem to play nice with SVG and is ignored
    #
    print_dpi = ("-Gdpi='%s'" % dpi) if output_format != "svg" else ""
    cmd = "dot -Gsize='%s' %s -T%s < %s" % (print_size,
                                            print_dpi, output_format, temp_dot_file_name)

    proc = subprocess.Popen(
        cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    result_str, error_str = proc.communicate()
    retcode = proc.returncode
    if retcode:
        raise subprocess.CalledProcessError(
            retcode, cmd + "\n" + "\n".join([str(result_str), str(error_str)]))

    #run_dot = os.popen(cmd)
    #result_str = run_dot.read()
    #err = run_dot.close()
    #
    # if err:
    #    raise RuntimeError("dot failed to run with exit code %d" % err)

    #
    #   wierd workaround for bug / bad interaction between firefox and svg:
    #           Font sizes have "px" appended.
    #

    if output_format == "svg":
        # result str is a binary string. I.e. could be .jpg
        # must turn it into string before we can replace, and then turn it back into binary
        result_str = result_str.decode()
        result_str = result_str.replace("0.12", "0.0px")
        result_str = result_str.encode()
    stream.write(result_str)


# _________________________________________________________________________________________

#   include_any_children

# _________________________________________________________________________________________
def include_any_children(nodes):
    """
    Get all children nodes by DFS in the inward direction,
    Ignores signals
    Also includes original nodes in the results
    """
    children_visitor = topological_sort_visitor(
        [], topological_sort_visitor.IGNORE_NODE_SIGNAL)
    depth_first_search(nodes, children_visitor, node._get_outward)
    return children_visitor.topological_sorted()


# _________________________________________________________________________________________

#   get_reachable_nodes

# _________________________________________________________________________________________
def get_reachable_nodes(nodes, children_as_well=True):
    """
    Get all nodes which are parents and children of nodes
        recursing through the entire tree

        i.e. go up *and* down tree starting from node

    1) specify parents_as_well = False
        to only get children and not parents of nodes
        """

    # look for parents of nodes and start there instead
    if children_as_well:
        nodes = include_any_children(nodes)

    parent_visitor = topological_sort_visitor(
        [], topological_sort_visitor.IGNORE_NODE_SIGNAL)
    depth_first_search(nodes, parent_visitor, node._get_inward)
    return parent_visitor.topological_sorted()


# _________________________________________________________________________________________

#   Helper functions to dump edges and nodes

# _________________________________________________________________________________________
def get_edges_str(name, edges):
    """
    helper function to dump edges as a list of names
    """
    edges_str = "  %d %s edges\n" % (len(edges), name)
    edges_str += "    " + \
        ", ".join([x_y[0]._name + "->" + x_y[1]._name for x_y in edges]) + "\n"
    return edges_str


def get_nodes_str(name, nodes):
    """
    helper function to dump nodes as a list of names
    """
    nodes_str = "  %s nodes = %d\n" % (name, len(nodes))
    nodes_str += "    " + ", ".join([x._name for x in nodes]) + "\n"
    return nodes_str
