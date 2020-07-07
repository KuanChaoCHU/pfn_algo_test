# -*- coding: utf-8 -*-
"""
Created on Mon May  4 
@author: KuanChao Chu
"""
import unittest
import itertools
import numpy as np
import problem1


class TestProblem1(unittest.TestCase):
    
    def setUp(self):
        self.p1 = problem1.Problem1()

    def _generate_all_matrix_combinations(self, x, y):
        """ Returns a list containing all possible matrix 
        """
        matrix_list = []
        for i in itertools.product([x, y], repeat=9):
            mat = np.array(i).reshape(3,3)
            matrix_list.append(mat)
        return matrix_list       

    def _count_matched_determinant(self, matrix_list, target_det, eps=1e-3):
        """ Calculate the determinant for each matrix in the list, then returns
            the number that its result matches target_det.
        """
        matched = 0
        for mat in matrix_list:
            det = np.linalg.det(mat)
            if abs(det - target_det) < eps:
                matched += 1
        return matched       
    
    def _prepare(self, case):
        """ Prepare the output provided by problem1.py (predict) and the ground-truth 
            calculated by this test module (answer). 
        """
        matrix_list = self._generate_all_matrix_combinations(case[0], case[1])
        answer = self._count_matched_determinant(matrix_list, case[2])
        predict = self.p1.solver(*case)
        return predict, answer

    def test_case0_easy(self):
        case = [0, 1, 2]    
        predict, answer = self._prepare(case)        
        self.assertEqual(predict, answer, 'Incorrect for case {}'.format(case))
        
    def test_case1_easy(self):
        case = [0, 1, 99]
        predict, answer = self._prepare(case)        
        self.assertEqual(predict, answer, 'Incorrect for case {}'.format(case))
        
    def test_case2_medium(self):
        case = [-4, -3, -3]
        predict, answer = self._prepare(case)        
        self.assertEqual(predict, answer, 'Incorrect for case {}'.format(case))
          
    def test_case3_medium(self):
        case = [2, 0, -8]
        predict, answer = self._prepare(case)        
        self.assertEqual(predict, answer, 'Incorrect for case {}'.format(case))
    
    def test_case4_hard(self):
        case = [-5, 3, -320]
        predict, answer = self._prepare(case)        
        self.assertEqual(predict, answer, 'Incorrect for case {}'.format(case))
        
    def test_case5_hard(self):
        case = [7, 4, 0]
        predict, answer = self._prepare(case)        
        self.assertEqual(predict, answer, 'Incorrect for case {}'.format(case))
                
        
if __name__ == '__main__':
    
    unittest.main()
    