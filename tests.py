import unittest

def run_unittests():
    ''' Execute Unit Tests '''
    tests = unittest.TestLoader().discover('tests/unit')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return False
    else:
        return True

def run_integration_tests():
    ''' Execute Integration Tests '''
    tests = unittest.TestLoader().discover('tests/integration')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return False
    else:
        return True

def run_functional_tests():
    ''' Execute Functional Tests '''
    tests = unittest.TestLoader().discover('tests/functional')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return False
    else:
        return True

if __name__ == '__main__':
    print("Test Runner: Unit tests")
    run_unittests()
    print("#" * 70)

    print("Test Runner: Integration tests")
    run_integration_tests()
    print("#" * 70)

    print("Test Runner: Functional tests")
    run_functional_tests()
    print("#" * 70)
