import unittest
import os
import coverage
import shutil


def test():
    tests = unittest.TestLoader().loadTestsFromName("test");
    unittest.TextTestRunner(verbosity=5).run(tests)

def cov():
    """Runs the unit tests with coverage."""
    cov = coverage.coverage(branch=True,
                            include='*', omit=[
                                            '*test*.py',
                                            '*/python2.7/*'
                                            ])
    cov.start()
    tests = unittest.TestLoader().loadTestsFromName("test");
    unittest.TextTestRunner(verbosity=5).run(tests)
    cov.stop()
    cov.save()
    print 'Coverage Summary:'

    cov.report()
    basedir = os.path.abspath(os.path.dirname(__file__))

    covdir = os.path.join(basedir, 'coverage')
    try:
        shutil.rmtree(covdir)
    except OSError:
        pass

    cov.html_report(directory=covdir)
    cov.erase()


if __name__ == '__main__':
    cov()
