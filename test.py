import unittest
from datetime import datetime

from smartmeter import Smartmeter


class SmartmeterTestCase(unittest.TestCase):
    def setUp(self):
        super(SmartmeterTestCase, self).setUp()
        self.api = Smartmeter(username="demouser", password="Demouser123")

    def tearDown(self):
        super(SmartmeterTestCase, self).tearDown()
        self.api.session.close()

    def test_confirm_login(self):
        """Confirm login"""
        self.assertTrue(len(self.api.profil()) > 0)

    def test_zaehlpunkte(self):
        """Confirm existence of zaehlpunkte with demo user"""
        zp = self.api.zaehlpunkte()
        self.assertTrue(len(zp) > 0)
        self.assertTrue(len(zp[0]["zaehlpunkte"]) > 0)

    def test_ereignisse(self):
        """Confirm existence of ereignisse with demo user"""
        eg_query = self.api.ereignisse(datetime(2021, 1, 1), datetime(2021, 1, 2))
        self.assertEqual(len(eg_query), 1)
        self.assertEqual(eg_query[0]["name"], "Wäsche waschen")


if __name__ == "__main__":
    unittest.main()
