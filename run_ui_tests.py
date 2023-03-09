import click
import unittest


@click.command()
@click.option('--path', default='ui_tests/sea-lion-app-q6nwz.ondigitalocean.app/sample1',
              help='Path to the directory containing the test files.')
def run_tests(path):
    """
    Runs all test cases in the specified directory.
    """
    loader = unittest.TestLoader()
    tests = loader.discover(path)
    testRunner = unittest.runner.TextTestRunner()
    testRunner.run(tests)


if __name__ == '__main__':
    run_tests()
