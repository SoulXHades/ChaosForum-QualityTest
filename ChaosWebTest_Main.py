import unittest
import LoginTest, RegistrationTest, ThreadTest, PostTest

def main():
    # suite = unittest.TestLoader().loadTestsFromModule(LoginTest)
    # unittest.TextTestRunner(verbosity=2).run(suite)

    suite = unittest.TestSuite()
    tests = unittest.TestLoader()
    suite.addTests(tests.loadTestsFromModule(LoginTest))
    suite.addTests(tests.loadTestsFromModule(ThreadTest))
    suite.addTests(tests.loadTestsFromModule(PostTest))
    suite.addTests(tests.loadTestsFromModule(RegistrationTest))
    unittest.TextTestRunner(verbosity=2).run(suite)


if __name__ == "__main__":
    main()