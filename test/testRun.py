import unittest
import os

def suite(): 
  suite = unittest.TestSuite()
	suite.addTest(TestCase('test1.py'))
	suite.addTest(TestCase('test2.py'))
	suite.addTest(TestCase('test3.py'))
	suite.addTest(TestCase('test4.py'))	
	suite.addTest(TestCase('test5.py'))
	suite.addTest(TestCase('test6.py'))
	return suite

class SuccessTest(unittest.TestCase): 
	def test_succ1(self): 
		os.system("python test1.py")
	def test_succ2(self):
		os.system("python test2.py")
	def test_succ3(self): 
		os.system("pyton test3.py")

class ExpectedFailureTestCase(unittest.TestCase): 
	def test_fail(self): 
		os.system("python test4.py")
	def test_fail2(self): 
		os.system("python test5.py")
	def test_fail3(self): 
		os.system("python test6.py")
		

if __name__ == '__main__': 
	unittest.main()
