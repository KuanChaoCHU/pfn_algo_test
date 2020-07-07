# -*- coding: utf-8 -*-
"""
Created on Mon May  4
@author: KuanChao Chu
"""
import os
import argparse
import time
import numpy as np


parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--input_path', type=str, default='q3_in.txt', help='the path of input file')
parser.add_argument('--output_path', type=str, default='q3_out.txt', help='the path of output file')
parser.add_argument('--show_elapsed_time', action='store_true', help='display time spent')
parser.add_argument('--manual_input', type=str, default=None, help='solve this manually added input instead (e.g. "6 2")')


class Node:
    
    def __init__(self, x):
        self.val = x
        self.prev = None
        self.next = None


class DLinkedList:
    
    def __init__(self, min_value, max_value):
        # dummy nodes: head and tail
        self.head = Node(min_value-1)  
        self.tail = Node(max_value+1)  
        self.head.next = self.tail
        self.tail.prev = self.head
        # memorized the last inserted node  
        self.curr = self.head
                        
    def insert(self, value):
        """ Inserts a new node
        """
        new_node = Node(value)
        ptr = self.search(value)        
        # ptr -> ptr.next to ptr -> new_node -> ptr.next
        new_node.next = ptr.next
        new_node.next.prev = new_node
        ptr.next = new_node
        new_node.prev = ptr        
        # update curr ptr
        self.curr = new_node
            
    def search(self, value):
        ptr = self.curr               
        while not (ptr.val < value < ptr.next.val):
            if value > ptr.next.val:
                ptr = ptr.next
            else:
                ptr = ptr.prev
        return ptr  
    
    def traversal(self):
        """ From head to tail
        """
        ptr = self.head.next
        trav = []
        while not ptr == self.tail:
            trav.append(ptr.val)
            ptr = ptr.next
        return trav


def priority_queue_push(queue, item):
    queue.append(item)
    priority_queue_bubble_up(queue, 0, len(queue)-1)    


def priority_queue_pop(queue):    
    root = queue[0]
    queue[0] = queue[-1]  # swap the last item to root 
    queue.pop()        
    if queue:
        priority_queue_bubble_down(queue, 0)            
    return root
   
    
def priority_queue_bubble_up(queue, rootIdx, idx):
    new_node = queue[idx]        
    while idx > rootIdx:
        parentIdx = (idx - 1) >> 1
        parent = queue[parentIdx]
        if new_node < parent:
            queue[idx] = parent
            idx = parentIdx
            continue
        break
    queue[idx] = new_node


def priority_queue_bubble_down(queue, idx):
    endIdx = len(queue)
    startIdx = idx
    new_node = queue[idx]
    # left child
    childIdx = 2*idx + 1    
    while childIdx < endIdx:
        rightIdx = childIdx + 1
        if rightIdx < endIdx and not queue[childIdx] < queue[rightIdx]:
            childIdx = rightIdx
        # swap smaller child up
        queue[idx] = queue[childIdx]
        idx = childIdx
        childIdx = 2*idx + 1
    queue[idx] = new_node
    priority_queue_bubble_up(queue, startIdx, idx)    
   
        
class Problem3:
    
    def __init__(self):
        self.opt, _ = parser.parse_known_args()
        self.inputs = self.load_inputs()
        self.longest = 0
        
    def load_inputs(self):
        """ Read and parse input cases from the .txt file.
        """
        with open(self.opt.input_path) as file:
            lines = file.readlines()
        lines = [[int(c) for c in line.rstrip().split()] for line in lines]
        return lines 

    def _timer(func):
        """ The timing function
        """
        def wrap3(self):
            begin = time.perf_counter()
            returned_value = func(self)
            end = time.perf_counter()
            if self.opt.show_elapsed_time:
                print("Problem 3 takes {:.3f} seconds".format(end - begin))
                print("The longest case takes {:.3f} seconds".format(self.longest))
            return returned_value
        return wrap3
    
    @_timer
    def get_solutions(self):
        """ Feeds the inputs line by line into the solver and outputs the results
            to a .txt file.
        """        
        cases = self.inputs
        answers = []
        for case in cases:
            n = case[0]
            a1 = case[1]
            answer = self.solver(n, a1)
            answers.append(answer)
        self._write_to_file(answers)
        return answers
    
    def solver(self, n, a1):
        """ Solves for a single input pair
        """
        # initialize
        start = time.perf_counter()
        queue = []
        dbl = DLinkedList(1, n)
        sit_order = []
        seat_index = np.arange(1, n+1)  # [1, 2, 3, ..., n], seat_index[i]=0 if occupied
        
        # inner functions 
        def push(pair):  # pair=(min_dist, seat_index)
            priority_queue_push(queue, (-1*pair[0], pair[1]))    
        
        def pop():
            out = priority_queue_pop(queue)
            return (-out[0], out[1])   
    
        def seat_occupied(idx):
            dbl.insert(idx)
            seat_index[idx-1] = 0
            sit_order.append(idx)
        
        # the first one
        seat_occupied(a1)        
        if a1 != 1:  
            push((a1-1,1))  
        if a1 != n:    
            push((n-a1,n))
        
        # loop until the queue is empty or terminal condition reached
        while True:        
            if not queue:
                break        
            
            next_min_dist, next_seat_index = pop()
            
            if next_min_dist <= 1:
                break            
            
            seat_occupied(next_seat_index)
                       
            if next_min_dist == 2:
                continue
            
            # find the nearest seat occupied on the left/right side            
            l_occ = dbl.curr.prev.val
            r_occ = dbl.curr.next.val
                        
            if l_occ != 0:
                l_cand = (next_seat_index + l_occ) // 2
            else:  # edge case: no occupied seat on left hand side
                l_cand = 1
            l_cand_min_dist = min((next_seat_index - l_cand), (l_cand - l_occ))    
            if l_cand_min_dist >= 2:
                push((l_cand_min_dist, l_cand))                
            
            if r_occ != (n+1):
                r_cand = (next_seat_index + r_occ) // 2                
            else:  # edge case: no occupied seat on right hand side
                r_cand = n
            r_cand_min_dist = min((r_cand - next_seat_index), (r_occ - r_cand))    
            if r_cand_min_dist >= 2:
                push((r_cand_min_dist, r_cand))      
         
        sum1 = np.array(sit_order)[1::2].astype('int64').sum()  # avoid int32 overflow    
        remain_seat_index = seat_index[seat_index>0].astype('int64')
        if len(sit_order) % 2 == 1:
            sum2 = remain_seat_index[0::2].sum()   
        else:
            sum2 = remain_seat_index[1::2].sum()     
        
        end = time.perf_counter()
        self.longest = max(self.longest, end - start)        
        return sum1 + sum2

    def _write_to_file(self, lines):
        if os.path.isfile(self.opt.output_path):
            print("Output file already exists!")
        else:
            lines = [str(line) + '\n' for line in lines]
            with open(self.opt.output_path, 'w') as file:
                file.writelines(lines) 
                
    def check_input_validity(self, raw_input):
        """ Check the input validity 
        """
        manual_input = [int(i) for i in raw_input.rstrip().split()]
        assert len(manual_input) == 2, 'invalid input!'
        assert 2<=manual_input[0]<=1000000, 'invalid input!'        
        assert 1<=manual_input[1]<=manual_input[0], 'invalid input!'
        return manual_input        


if __name__ == '__main__':
    
    p3 = Problem3()
    if p3.opt.manual_input is None:
        sol = p3.get_solutions()
    else:
        manual_input = p3.check_input_validity(p3.opt.manual_input)
        print('Output: {}'.format(p3.solver(*manual_input)))
