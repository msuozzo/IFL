import unittest
import os


class SuccessTest(unittest.TestCase): 
	def test_succ1(self): 
		os.system("python compiler.py examples/ex1.ifl")
	def test_succ2(self):
		os.system("python compiler.py examples/ex2.ifl")
	def test_succ3(self): 
		os.system("python compiler.py examples/ex3.ifl")

class ExpectedFailureTestCase(unittest.TestCase): 
	def test_fail(self): 
		os.system("python compiler.py test/test4.ifl")
	def test_fail2(self): 
		os.system("python compiler.py test/test5.ifl")
	def test_fail3(self):
		os.system("python compiler.py test/test6.ifl")
	def test_fail4(self): 
		os.system("python compiler.py test/test7.ifl")
	def test_file5(self): 
		os.system("python compiler.py test/test8.ifl")
	def test_file6(self): 
		os.system("python compiler.py test/test9.ifl")
		

if __name__ == '__main__': 
	unittest.main()
