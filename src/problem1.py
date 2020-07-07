# -*- coding: utf-8 -*-
"""
Created on Mon May  4
@author: KuanChao Chu
"""
import os
import argparse
import time


parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--input_path', type=str, default='q1_in.txt', help='the path of input file')
parser.add_argument('--output_path', type=str, default='q1_out.txt', help='the path of output file')
parser.add_argument('--show_elapsed_time', action='store_true', help='display time spent')
parser.add_argument('--manual_input', type=str, default=None, help='solve this manually added input instead (e.g. "0 1 2")')


class Problem1:

    def __init__(self):
        self.opt, _ = parser.parse_known_args()
        self.inputs = self.load_inputs()

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
        def wrap1(self):
            begin = time.perf_counter()
            returned_value = func(self)
            end = time.perf_counter()
            if self.opt.show_elapsed_time:
                print("Problem 1 takes {:.3f} seconds".format(end - begin))
            return returned_value
        return wrap1

    @_timer
    def get_solutions(self):
        """ Feeds the inputs line by line into the solver and outputs the results
            to a .txt file.
        """
        cases = self.inputs
        answers = []
        for case in cases:
            x = case[0]
            y = case[1]
            det = case[2]
            answer = self.solver(x, y, det)
            answers.append(answer)
        self._write_to_file(answers)
        return answers

    def solver(self, x, y, target_det):
        """ Solves for a single input pair and returns the number of 
            matched combinations.
        |a b c|
        |d e f|  = aei + bfg + cdh - ceg - bdi - afh
        |g h i|

        config is a string consists of '0' and '1'. '0' stands for x and '1' stands
        for y at location a~i in order.
        """
        matched = 0
        for i in range(2**9):
            config = '{0:09b}'.format(i)
            mat = [x if c == '0' else y for c in config]
            det = mat[0]*(mat[4]*mat[8] - mat[5]*mat[7]) +\
                  mat[1]*(mat[5]*mat[6] - mat[3]*mat[8]) +\
                  mat[2]*(mat[3]*mat[7] - mat[4]*mat[6])

            if det == target_det:
                matched += 1

        return matched

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
        assert -10<=manual_input[0]<=10, 'invalid input!'
        assert -10<=manual_input[1]<=10, 'invalid input!'
        assert manual_input[0]!=manual_input[1], 'invalid input!'
        assert -1000<=manual_input[2]<=1000, 'invalid input!'
        return manual_input
        

if __name__ == '__main__':

    p1 = Problem1()
    if p1.opt.manual_input is None:
        sol = p1.get_solutions()
    else:
        manual_input = p1.check_input_validity(p1.opt.manual_input)
        print('Output: {}'.format(p1.solver(*manual_input)))        
        