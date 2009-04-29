#!/usr/bin/env python2.5
################################################################################
#
#   adjacent_pairs_iterate.py
# 
# 
#       iterate successive pairs in a list or tuple
#
#
#   Copyright (C) 2007 Leo Goodstadt
#
#   This program is free software; you can redistribute it and/or
#   modify it under the terms of the GNU General Public License
#   as published by the Free Software Foundation; version 2
#   of the License
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program; if not, write to the Free Software
#   Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#################################################################################


from itertools import izip
def adjacent_pairs_iterate (array, reverse = False):
    """
    returns pairs of iterators to successive positions
    """
    if len(array) < 2:
        return
       
    # get iterators to successive positions
    if reverse:
        curr = reversed(array)
        next = reversed(array)
    else:
        curr = iter(array)
        next = iter(array)
    next.next() 
    for i, j in izip(curr, next):
        yield i, j    
    

def unit_test():
    numbers = range(10)
    print "Forward"
    for i, j in adjacent_pairs_iterate(numbers):
        print i, j
    print "Reversed"
    for i, j in adjacent_pairs_iterate(numbers, reverse=True):
        print i, j
    print numbers
        
if __name__ == '__main__':
    unit_test()




