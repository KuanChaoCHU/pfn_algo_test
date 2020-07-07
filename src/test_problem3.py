# -*- coding: utf-8 -*-
"""
Created on Mon May  4
@author: KuanChao Chu
"""
import unittest
import numpy as np
import problem3


class TestProblem3(unittest.TestCase):
    
    def setUp(self):
        self.p3 = problem3.Problem3()
    
    def _calculate_ground_truth_by_brute_force(self, n, a1):
        """ Brute-force solution: O(n^3)
            min_dist[i] represents the minimal distance between point i 
            and all the occupied seats.
            The position with largest min_dist[i] will be picked as sit_next, after 
            a round of min_dist calculation is finished.
            
            Consequently, we can update the occupied and sit_order list, and so on.            
        """
        sit_order = []
        occupied = [0] * n
        
        sit_order.append(a1)   
        occupied[a1-1] = 1      
        for i in range(1, n):
            min_dist = [0] * n
            for j in range(n):
                if occupied[j] == 0:  # calculate min_dist for evey empty seat
                    min_dist_j = n
                    for k in range(n):
                        if occupied[k] == 1:
                            min_dist_j = min(min_dist_j, abs(j-k))
                    min_dist[j] = min_dist_j 
            
            min_dist = np.array(min_dist)
            sit_next = min_dist.argmax()
            
            sit_order.append(sit_next+1)
            occupied[sit_next] = 1
                
        return np.array(sit_order)[1::2].astype('int64').sum()
        
    def _prepare(self, case):
        """ Prepare the output provided by problem3.py (predict) and the ground-truth 
            calculated by this test module (answer). 
        """
        n = case[0]
        a1 = case[1]
        answer = self._calculate_ground_truth_by_brute_force(n, a1)
        predict = self.p3.solver(n, a1)
        return predict, answer
        
    def test_case_base(self):
        case = [6, 2]
        predict, answer = self._prepare(case)         
        self.assertEqual(predict, answer, 'Incorrect for case {}'.format(case))
        
    def test_case_edge(self):
        n = 2
        for i in range(n):
            with self.subTest(i=i):
                case = [n, i+1]
                predict, answer = self._prepare(case)         
                self.assertEqual(predict, answer, 'Incorrect for case {}'.format(case))        
            
    def test_n_15_all_possible_a1(self):
        n = 15
        for i in range(n):
            with self.subTest(i=i):
                case = [n, i+1]
                predict, answer = self._prepare(case)         
                self.assertEqual(predict, answer, 'Incorrect for case {}'.format(case))    
        
    def test_n_37_all_possible_a1(self):
        n = 37
        for i in range(n):
            with self.subTest(i=i):
                case = [n, i+1]
                predict, answer = self._prepare(case)         
                self.assertEqual(predict, answer, 'Incorrect for case {}'.format(case))    
         
    def test_n_90_all_possible_a1(self):
        n = 90
        for i in range(n):
            with self.subTest(i=i):
                case = [n, i+1]
                predict, answer = self._prepare(case)         
                self.assertEqual(predict, answer, 'Incorrect for case {}'.format(case))    
          
        
if __name__ == '__main__':
    
    unittest.main()
