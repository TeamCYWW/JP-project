import main
import threading
import time
import signal
import unittest
import psycopg2
import Algorithm


class TestThread(threading.Thread):
    def __init__(self):
        """
        class initiator
        """
        threading.Thread.__init__(self)

    def run(self):
        time.sleep(2)
        print "finish thread"


class WrongTestCase(unittest.TestCase):
    def setUp(self):
        self.app = main.APP.test_client()

    def tearDown(self):
        print "done"
        # try:
        #     self.a.close()
        # except Exception as e:
        #     print "No open database to close"

    def test_before_request_wrong(self):
        with main.APP.test_request_context():
            main.ENGINE = "some wrong request"
            main.before_request()
            main.handle_b()

    def test_get_price(self):
        self.app.get('/get_price')
        print "successfully get test"

    def test_b(self):
        rv = self.app.get('/b')
        print "successfully b"

    def test_submit(self):
        with main.APP.test_request_context():
            main.new_thread = TestThread()
            main.new_thread.start()
            print "Print if thread is alive: ",
            print main.new_thread.isAlive()
            main.is_trading()
            main.handle_submit()

    def test_is_trading(self):
        rv = self.app.get('/is_trading')
        assert rv is not None
        print "sccessfully get trading status"

    def test_wrong_reg(self):
        with main.APP.test_request_context():
            main.data_config = "some wrong request"
            self.app.post('/register', data=dict(username="asdf", password="asdf"))
            print "pass test to wrong register"

    def test_wrong_del(self):
        with main.APP.test_request_context():
            main.data_config = "some wrong request"
            self.app.post('/del_user', data=dict(username="asdf"))
            print "pass test to wrong register"

    def test_wrong_login(self):
        self.app.post('/login', data=dict(
            username="dakfjl",
            password="qeoij"))
        print "pass test wrong login"


class FlaskrTestCase(unittest.TestCase):
    def setUp(self):
        self.app = main.APP.test_client()

    def tearDown(self):
        print "done"
        # try:
        #     self.a.close()
        # except Exception as e:
        #     print "No open database to close"

    # def test_before_request_wrong(self):
    #     with main.APP.test_request_context():
    #         main.ENGINE = "some wrong request"
    #         main.before_request()

    def test_empty_db(self):
        rv = self.app.get('/')
        print "access log page"

    def test_index(self):
        rv = self.app.get('/index')
        print "access main page"

    def register(self, username, password):
        return self.app.post('/register', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    def real_register(self):
        rv = self.app.post('/del_user', data=dict(
            username='newuser',
        ), follow_redirects=True)
        assert '1' in rv.data
        print "delete user data"
        rv = self.register('newuser', 'default')
        assert '1' in rv.data
        print "successfully register"

    def login(self, username, password):
        return self.app.post('/login', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    def test_login(self):
        self.real_register()
        rv = self.login('newuser', 'default')
        print "this is test_login ",
        print rv
        assert '1' in rv.data
        rv = self.login('xxxx', '12345')
        assert '2' in rv.data
        print "all login are passed"
        rv = self.app.post('/del_user', data=dict(
            username='admin',
        ), follow_redirects=True)
        assert '1' in rv.data
        print "delete user data"

    def test_get_price(self):
        rv = self.app.get('/get_price')
        print "sccessfully get test"

    def test_sell(self):
        rv = self.app.post('/submit', data=dict(
            quantity=100,
        ), follow_redirects=True)
        assert '1' in rv.data
        with main.APP.test_request_context():
            main.query = "some thing wrong with request"
            main.get_price()
            self.app.get('/get_price')
            print "bad query test for get_price"

    def test_del_b(self):
        print "I'm testing history"
        rv = self.app.get('/b', data=dict(
            page='1', row='10'
        ))
        assert type(rv.data[0]) is str
        print "sccessfully get history"

    def test_del(self):
        rv = self.app.post('/del_user', data=dict(
            username='newuser',
        ), follow_redirects=True)
        assert '1' in rv.data
        print "delete user data"

    def test_exit(self):
        try:
            main.original_sigint = signal.getsignal(signal.SIGINT)
            signal.signal(signal.SIGINT, main.exit_gracefully(1,2))
        except SystemExit:
            print "pass exit test"

    def test_crossdomain(self):
        rv = main.crossdomain(1,["asd","asdfaw",[32,12]],3,4,5,6)

    def test_history(self):
        rv = self.app.get('/reg')
        assert rv is not None
        print "sccessfully get regpage"

    def test_submit(self):
        rv = self.app.get('/submit?quantity=10')
        assert rv is not None
        print "sccessfully get submit"

    def test_is_trading(self):
        rv = self.app.get('/is_trading')
        assert rv is not None
        print "sccessfully get trading status"


class AlgoTestToFail(unittest.TestCase):
    def setUp(self):
        self.instance = Algorithm.UseThread(10)

    def tearDown(self):
        self.instance = None

    def test_quote_fail(self):
        Algorithm.quote_query = "some wrong query {}"
        try:
            Algorithm.UseThread.quote_info()
        except SystemExit:
            print "successfully test quote_info method"

    def test_db_fail(self):
        Algorithm.db_link = "some wrong db link"
        self.assertEqual(Algorithm.UseThread.connect_database(), 1)
        print "successfully test connect_database method fail"


class AlgoTestCase(unittest.TestCase):
    def setUp(self):
        self.instance = Algorithm.UseThread(10)

    def tearDown(self):
        self.instance = None

    def test_cal_current_time(self):
        self.assertEqual(self.instance.cal_current_time('2016-12-10 08:12:49.510760'), 29569.510760,
                         'incorrect Time calculation')
        try:
            self.instance.cal_current_time('2016-12-10 08:40:49.510760')
        except SystemExit as info:
            print info

    def test_cal_interval_time(self):
        self.assertEqual(self.instance.cal_interval_time(10000, 500, 100), 4000,
                         'incorrect Time calculation')
        self.assertEqual(self.instance.cal_interval_time(39000, 500, 100), 0,
                         'incorrect Time calculation')

    def set_up(self):
        connection = self.instance.connect_database()
        assert connection != 1
        print "connect to database"
        return connection

    def test_database_clean(self):
        connection = self.set_up()
        cursor = connection.cursor()
        self.instance.database_cleanup(connection, cursor)
        print "database cleaned"
        self.instance.database_cleanup(connection, None)
        print "Test to fail clean database"

    def test_database_insert(self):
        # conn = psycopg2.connect("host='localhost' dbname='stock' user='postgres' password=''")
        # cursor = conn.cursor()
        conn = self.set_up()
        cursor = conn.cursor()
        cursor.execute('SELECT count(*) FROM transact')
        row_count = 0
        for row in cursor:
            row_count += 1
            print "row: %s    %s\n" % (row_count, row)
        sell_info = {'trans_id': 12, 'total_sell': 0, 'sum_value': 0.0, 'avg': 0.0, 'plan_value': 10000}
        self.instance.insert_trans(sell_info, "failure occurred, recalculate strategy", None, cursor, conn)
        try:
            self.instance.insert_trans(sell_info, "failure occurred, recalculate strategy", None, None, conn)
        except SystemExit as info:
            print info
            print "Pass exception test"

    def test_quote_info(self):
        rv = self.instance.quote_info()
        print rv

    def test_make_order(self):
        market_info = {'top_bid': {'price': 104}}
        rv = self.instance.make_order(100, market_info, 10)
        print rv
        market_info = {'top_bid': {'price': 9999999}}
        rv = self.instance.make_order("hello", market_info, -20)
        print rv

    def test_run(self):
        self.instance.run()
        self.instance = Algorithm.UseThread(0)
        self.instance.run()
        self.instance = Algorithm.UseThread(30)
        self.instance.run()
        self.instance = Algorithm.UseThread(10000000)
        self.instance.run()

if __name__ == '__main__':
    unittest.main()
