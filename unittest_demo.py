
import unittest
class TestCase_01(unittest.TestCase): # 继承unittest.TestCase
 
    @classmethod
    def setUpClass(cls):
        print('这是所有case的前置条件01')
 
    @classmethod
    def tearDownClass(cls):
        print('这是所有case的后置条件01')
 
    def setUp(self):
        print('这是每条case的前置条件01')
 
    def tearDown(self):
        print('这是每条case的后置条件01')
 
    def testThird_01(self): # 测试用例的命名必须以test开头，否则不予执行
        print('01: 第三条case')
 
    def testFirst_01(self): 
        print('01: 第一条case')
 
    @unittest.skip('不执行这条case') # 跳过这条case
    def testSecond_01(self):
        print('01: 第二条case') 
 
    def testFourth_01(self):
        print('01: 第四条case') 
 
if __name__ == '__main__':
    # unittest.main() # 使用main()直接运行时，将按case的名称顺序执行
    suite = unittest.TestSuite()
    suite.addTest(TestCase_01('testThird_01')) # 将需要执行的case添加到Test Suite中，没有添加的不会被执行
    suite.addTest(TestCase_01('testSecond_01'))
    suite.addTest(TestCase_01('testFirst_01'))
    unittest.TextTestRunner().run(suite) # 将根据case添加的先后顺序执行
