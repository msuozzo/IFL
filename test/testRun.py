import unittest
import os

def suite(): 
  suite = unittest.TestSuite()
	suite.addTest(TestCase('test-1.py'))
	suite.addTest(TestCase('test-2.py'))
	suite.addTest(TestCase('test-3.py'))
	suite.addTest(TestCase('test-4.py'))	
	suite.addTest(TestCase('test-5.py'))
	suite.addTest(TestCase('test-6.py'))
	return suite

class SuccessTest(unittest.TestCase): 
	def test_succ1(self): 
		os.system("python test-1.py")
	def test_succ2(self):
		os.system("python test-2.py")
	def test_succ3(self): 
		os.system("pyton test-3.py")

class ExpectedFailureTestCase(unittest.TestCase): 
	def test_fail(self): 
		os.system("python test-4.py")
	def test_fail2(self): 
		os.system("python test-5.py")
	def test_fail3(self): 
		os.system("python test-6.py")
		

if __name__ == '__main__': 
	unittest.main()
 
