import unittest

loader = unittest.TestLoader()
tests = loader.discover('ui_tests')
testRunner = unittest.runner.TextTestRunner()
testRunner.run(tests)
