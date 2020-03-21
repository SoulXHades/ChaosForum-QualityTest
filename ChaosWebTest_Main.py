import unittest
import LoginTest, RegistrationTest, ThreadTest, PostTest

import HtmlTestRunner
import os

def main():
    suite = unittest.TestSuite()
    tests = unittest.TestLoader()
    suite.addTests(tests.loadTestsFromModule(LoginTest))
    suite.addTests(tests.loadTestsFromModule(ThreadTest))
    suite.addTests(tests.loadTestsFromModule(PostTest))
    suite.addTests(tests.loadTestsFromModule(RegistrationTest))
    unittest.TextTestRunner(verbosity=2).run(suite)
    
    
    curr_dir = os.getcwd()
    runner = HtmlTestRunner.HTMLTestRunner(
        output=curr_dir+"/Report",
        report_title='Chaos Test Report',
        report_name='ChaosTestReport',
        combine_reports=True,
    )
    runner.run(suite)

if __name__ == "__main__":
    main()