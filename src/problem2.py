# -*- coding: utf-8 -*-
"""
Created on Tue May  5
@author: KuanChao Chu
"""
import os
import argparse
import time
import numpy as np


parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--input_path', type=str, default='q2_in.txt', help='the path of input file')
parser.add_argument('--output_path', type=str, default='q2_out.txt', help='the path of output file')
parser.add_argument('--show_elapsed_time', action='store_true', help='display time spent')
parser.add_argument('--manual_input', type=str, default=None, help='solve this manually added input instead (e.g. "5 2 3")')


class Problem2:
    
    def __init__(self):
        self.opt, _ = parser.parse_known_args()
        self.inputs = self.load_inputs()        
        # memoization
        self.abc_count_tbl = self.calculate_abc_count()
        self.len_s_tbl = self.calculate_string_length()
        
    def load_inputs(self):
        """ Read and parse input cases from the .txt file.
        """
        with open(self.opt.input_path) as file:
            lines = file.readlines()
        lines = [[int(c) for c in line.rstrip().split()] for line in lines]
        return lines 

    def calculate_abc_count(self):
        """ Calcuate the numbers of a, b, and c for each string s_i,
            where 1<=i<=50. These numbers are acquired following the same equation
            s_i = s_(i-3) + s_(i-2) + s_(i-1). A table abc_count of shape (50,3),
            which stores the numbers for string s_i as abc_count[i-1] will be returned.  
        """
        count_abc = np.zeros(shape=(50, 3), dtype='int64')  # int32 may overflow
        # initialize: s_1='a', s_2='b', s_3='c'
        count_abc[0][0] = 1
        count_abc[1][1] = 1
        count_abc[2][2] = 1
        
        for i in range(3, 50):
            count_abc[i] = count_abc[i-3] + count_abc[i-2] + count_abc[i-1]
        return count_abc

    def calculate_string_length(self):
        """
        """
        len_s = [1, 1, 1]
        for i in range(3, 50):
            length = len_s[i-3] + len_s[i-2] + len_s[i-1]
            len_s.append(length)
        return len_s

    def _timer(func):
        """ The timing function
        """
        def wrap2(self):
            begin = time.perf_counter()
            returned_value = func(self)
            end = time.perf_counter()
            if self.opt.show_elapsed_time:
                print("Problem 2 takes {:.3f} seconds".format(end - begin))
            return returned_value
        return wrap2

    @_timer
    def get_solutions(self):
        """ Feeds the inputs line by line into the solver and outputs the results
            to a .txt file.
        """        
        cases = self.inputs
        answers = []
        for case in cases:
            k = case[0]
            p = case[1]
            q = case[2]
            answer = self.solver(k, p, q)
            answers.append('Output: a:{},b:{},c:{}'.format(*answer))
        self._write_to_file(answers)
        return answers
     
    def solver(self, k, p, q):
        """ Solves for a single input pair and returns the count of a, b, and c in 
            the ndarray.        
        # section 1 range: 1~len_s[k-4]
        # section 2 range: len_s[k-4] + 1 ~ len_s[k-4] + len_s[k-3]
        # section 3 range: len_s[k-4] + len_s[k-3] + 1 ~ len_s[k-1]
        """
        # base case
        if p == 1 and q == self.len_s_tbl[k-1]:
            return self.abc_count_tbl[k-1]
        
        if p <= self.len_s_tbl[k-4]:
            if q <= self.len_s_tbl[k-4]:
                return self.solver(k-3, p, q)
            elif q <= (self.len_s_tbl[k-4] + self.len_s_tbl[k-3]):
                return self.solver(k-3, p, self.len_s_tbl[k-4]) +\
                       self.solver(k-2, 1, q-(self.len_s_tbl[k-4]))
            else:
                return self.solver(k-3, p, self.len_s_tbl[k-4]) +\
                       self.solver(k-2, 1, self.len_s_tbl[k-3]) +\
                       self.solver(k-1, 1, q - (self.len_s_tbl[k-4] + self.len_s_tbl[k-3]))           
        elif p <= (self.len_s_tbl[k-4] + self.len_s_tbl[k-3]):
            if q <= (self.len_s_tbl[k-4] + self.len_s_tbl[k-3]):
                return self.solver(k-2, p - (self.len_s_tbl[k-4]), q - (self.len_s_tbl[k-4]))
            else:
                return self.solver(k-2, p - (self.len_s_tbl[k-4]), self.len_s_tbl[k-3]) +\
                       self.solver(k-1, 1, q- (self.len_s_tbl[k-4] + self.len_s_tbl[k-3]))        
        else:
            return self.solver(k-1, p - (self.len_s_tbl[k-4] + self.len_s_tbl[k-3]), q - (self.len_s_tbl[k-4] + self.len_s_tbl[k-3]))
    
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
        assert len(manual_input) == 3, 'invalid input!'
        assert 1<=manual_input[0]<=50, 'invalid input!'
        assert 1<=manual_input[1]<=manual_input[2]<=self.len_s_tbl[manual_input[0]-1], 'invalid input!'
        return manual_input


if __name__ == '__main__':
    
    p2 = Problem2()
    if p2.opt.manual_input is None:
        sol = p2.get_solutions()
    else:
        manual_input = p2.check_input_validity(p2.opt.manual_input)
        print('Output: a:{},b:{},c:{}'.format(*p2.solver(*manual_input)))      
