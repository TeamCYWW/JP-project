import unittest
import main
import signal

class MyTest(unittest.TestCase):

    # def setUp(self):
    #     self.app = main.APP.test_client()
    #
    # def tearDown(self):
    #     print "done"

    def test_first_case(self):
        with main.APP.test_request_context():
            # main.last_request_num = 999
            main.ENGINE = "some wrong request"
            main.before_request()
            # try:
            #     main.original_sigint = signal.getsignal(signal.SIGINT)
            #     signal.signal(signal.SIGINT, main.exit_gracefully(1,2))
            #     main.get_price()
            # except SystemExit:
            #     print "pass exit test"


if __name__ == '__main__':
    unittest.main()
