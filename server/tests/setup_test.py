from app import app
from urllib import request
from flask_testing import LiveServerTestCase


class MyTest(LiveServerTestCase):
    def create_app(self):
        app.config['TESTING'] = True
        return app

    def test_server_is_up_and_running(self):
        response = request.urlopen(self.get_server_url())
        self.assertEqual(response.code, 200)
