# -*- coding: utf-8 -*-
"""
Created on Tue May  5
@author: KuanChao Chu
"""
import unittest
import numpy as np
import problem2


class TestProblem2(unittest.TestCase):
    
    def setUp(self):
        self.p2 = problem2.Problem2()
        self.max_k = 14
        self.string_tbl = self.generate_string_table()
        
    def generate_string_table(self):
        """ Generates and stores the strings until k=max_k
            (since the length growth is fast, we can't generate all of them)
        """
        string_s = ['a', 'b', 'c']
        for i in range(3, self.max_k):
            string_s.append(string_s[i-3] + string_s[i-2] + string_s[i-1])       
        return string_s
    
    def _prepare(self, case):
        """ Prepare the output provided by problem2.py (predict) and the ground-truth 
            calculated by this test module (answer). 
        """
        count_a = self.string_tbl[case[0]-1][(case[1]-1):(case[2])].count('a')
        count_b = self.string_tbl[case[0]-1][(case[1]-1):(case[2])].count('b')
        count_c = self.string_tbl[case[0]-1][(case[1]-1):(case[2])].count('c')
        answer = 'a:{},b:{},c:{}'.format(count_a, count_b, count_c)
        predict = 'a:{},b:{},c:{}'.format(*self.p2.solver(*case))
        return predict, answer

    def test_case_base(self):
        case = [5, 2, 3]
        predict, answer = self._prepare(case)         
        self.assertEqual(predict, answer, 'Incorrect for case {}'.format(case))
        
    def test_case_substring_only_in_section_1(self):
        case = [12, 15, 54]
        predict, answer = self._prepare(case)         
        self.assertEqual(predict, answer, 'Incorrect for case {}'.format(case))
        
    def test_case_substring_only_in_section_2(self):
        case = [11, 43, 77]
        predict, answer = self._prepare(case)         
        self.assertEqual(predict, answer, 'Incorrect for case {}'.format(case))
        
    def test_case_substring_only_in_section_3(self):    
        case = [13, 333, 500]
        predict, answer = self._prepare(case)         
        self.assertEqual(predict, answer, 'Incorrect for case {}'.format(case))
        
    def test_case_substring_across_section_1_2(self):    
        case = [10, 8, 40]
        predict, answer = self._prepare(case)         
        self.assertEqual(predict, answer, 'Incorrect for case {}'.format(case))     

    def test_case_substring_across_section_2_3(self):    
        case = [12, 189, 341]
        predict, answer = self._prepare(case)         
        self.assertEqual(predict, answer, 'Incorrect for case {}'.format(case)) 
        
    def test_case_substring_across_section_1_2_3(self):    
        case = [8, 3, 31]
        predict, answer = self._prepare(case)         
        self.assertEqual(predict, answer, 'Incorrect for case {}'.format(case)) 
        
    def test_case_edgecase_1(self):    
        case = [10, 17, 17]
        predict, answer = self._prepare(case)         
        self.assertEqual(predict, answer, 'Incorrect for case {}'.format(case))     
        
    def test_case_edgecase_2(self):    
        case = [6, 4, 4]
        predict, answer = self._prepare(case)         
        self.assertEqual(predict, answer, 'Incorrect for case {}'.format(case))    
        
    def test_case_edgecase_3(self):    
        case = [7, 16, 17]
        predict, answer = self._prepare(case)         
        self.assertEqual(predict, answer, 'Incorrect for case {}'.format(case))     
        
    def test_case_random(self):    
        for i in range(1000):
            with self.subTest(i=i):
                k = np.random.randint(1, self.max_k)
                q = np.random.randint(1, len(self.string_tbl[k-1])+1)
                p = np.random.randint(1, q+1)
                case = [k, p, q]
                predict, answer = self._prepare(case)         
                self.assertEqual(predict, answer, 'Incorrect for case {}'.format(case))    
        
        
if __name__ == '__main__':
    
    unittest.main()



