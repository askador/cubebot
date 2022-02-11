import unittest

from translation_test import TestTranslationFormat



def suite():
    suite = unittest.TestSuite()

    suite.addTest(unittest.makeSuite(TestTranslationFormat))

    return suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    test_suite = suite()
    runner.run(test_suite)