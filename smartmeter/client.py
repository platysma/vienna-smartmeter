"""Contains the Smartmeter API Client."""
import logging
from datetime import datetime
from urllib import parse

import requests
from lxml import html

from .errors import SmartmeterLoginError

logger = logging.getLogger(__name__)


class Smartmeter:
    """Smartmeter client."""

    API_URL = "https://service.wienernetze.at/rest/smp/1.0/"
    API_DATE_FORMAT = "%Y-%m-%dT%H:%M:%S.%f"
    AUTH_URL = "https://service.wienerstadtwerke.at/auth/realms/wienernetze/protocol/openid-connect/"  # noqa

    def __init__(self, username, password, login=True):
        """Access the Smartmeter API.

        Args:
            username (str): Username used for API Login.
            password (str): Username used for API Login.
            login (bool, optional): If _login() should be called. Defaults to True.
        """
        self.username = username
        self.password = password
        self.session = requests.Session()

        if login:
            self._login()

    def _login(self):
        args = {
            "client_id": "client-smp-public",
            "redirect_uri": "https://www.wienernetze.at/wnapp/smapp/",
            "response_mode": "fragment",
            "response_type": "code",
            "scope": "openid",
            "nonce": "",
            "prompt": "login",
        }
        login_url = self.AUTH_URL + "auth?" + parse.urlencode(args)
        result = self.session.get(login_url)
        tree = html.fromstring(result.content)
        action = tree.xpath("(//form/@action)")[0]

        result = self.session.post(
            action,
            data={
                "username": self.username,
                "password": self.password,
            },
            allow_redirects=False,
        )

        if "Location" not in result.headers:
            raise SmartmeterLoginError("Login failed. Check username/password.")

        code = result.headers["Location"].split("&code=", 1)[1]

        result = self.session.post(
            self.AUTH_URL + "token",
            data={
                "code": code,
                "grant_type": "authorization_code",
                "client_id": "client-smp-public",
                "redirect_uri": "https://www.wienernetze.at/wnapp/smapp/",
            },
        )

        self.access_token = result.json()["access_token"]

    def _dt_string(self, datetime_string):
        return datetime_string.strftime(self.API_DATE_FORMAT)[:-3] + "Z"

    def _call_api(
        self,
        endpoint,
        base_url=None,
        method="GET",
        data=None,
        query=None,
        return_response=False,
    ):
        if base_url is None:
            base_url = self.API_URL
        url = "{0}{1}".format(base_url, endpoint)

        if query:
            url += ("?" if "?" not in endpoint else "&") + parse.urlencode(query)

        logger.debug("REQUEST: {}", url)

        headers = {
            "Authorization": f"Bearer {self.access_token}",
        }

        if data:
            logger.debug("DATA: {}", data)
            headers["Content-Type"] = "application/json"

        response = self.session.request(method, url, headers=headers, json=data)

        if return_response:
            return response

        return response.json()

    def _get_first_zaehlpunkt(self):
        return self.zaehlpunkte()[0]["zaehlpunkte"][0]["zaehlpunktnummer"]

    def zaehlpunkte(self):
        """Returns zaehlpunkte for currently logged in user."""
        return self._call_api("m/zaehlpunkte")

    def verbrauch_raw(self, date_from, date_to=None, zaehlpunkt=None):
        """Returns energy usage.

        Args:
            date_from (datetime): Start date for energy usage request
            date_to (datetime, optional): End date for energy usage request.
                Defaults to datetime.now().
            zaehlpunkt (str, optional): Id for desired smartmeter.
                If None check for first meter in user profile.

        Returns:
            dict: JSON response of api call to
                'm/messdaten/zaehlpunkt/ZAEHLPUNKT/verbrauchRaw'
        """
        if date_to is None:
            date_to = datetime.now()
        if zaehlpunkt is None:
            zaehlpunkt = self._get_first_zaehlpunkt()
        endpoint = "m/messdaten/zaehlpunkt/{}/verbrauchRaw".format(zaehlpunkt)
        query = {
            "dateFrom": self._dt_string(date_from),
            "dateTo": self._dt_string(date_to),
            "granularity": "DAY",
        }
        return self._call_api(endpoint, query=query)

    def verbrauch(self, date_from, date_to=None, zaehlpunkt=None):
        """Returns energy usage.

        Args:
            date_from (datetime.datetime): Starting date for energy usage request
            date_to (datetime.datetime, optional): Ending date for energy usage request.
                Defaults to datetime.datetime.now().
            zaehlpunkt (str, optional): Id for desired smartmeter.
                If None check for first meter in user profile.

        Returns:
            dict: JSON response of api call to
                'm/messdaten/zaehlpunkt/ZAEHLPUNKT/verbrauch'
        """
        if date_to is None:
            date_to = datetime.now()
        if zaehlpunkt is None:
            zaehlpunkt = self._get_first_zaehlpunkt()
        endpoint = "m/messdaten/zaehlpunkt/{}/verbrauch".format(zaehlpunkt)
        query = {
            "dateFrom": self._dt_string(date_from),
            "dateTo": self._dt_string(date_to),
            "period": "DAY",
            "accumulate": False,
            "offset": 0,
            "dayViewResolution": "QUARTER-HOUR",
        }
        return self._call_api(endpoint, query=query)

    def profil(self):
        """Returns profil of logged in user.

        Returns:
            dict: JSON response of api call to 'w/user/profile'
        """
        return self._call_api("w/user/profile")

    def ereignisse(self, date_from, date_to=None, zaehlpunkt=None):
        """Returns events between date_from and date_to of a specific smart meter.

        Args:
            date_from (datetime.datetime): Starting date for request
            date_to (datetime.datetime, optional): Ending date for request.
                Defaults to datetime.datetime.now().
            zaehlpunkt (str, optional): Id for desired smart meter.
                If is None check for first meter in user profile.

        Returns:
            dict: JSON response of api call to 'w/user/ereignisse'
        """
        if date_to is None:
            date_to = datetime.now()
        if zaehlpunkt is None:
            zaehlpunkt = self._get_first_zaehlpunkt()
        query = {
            "zaehlpunkt": zaehlpunkt,
            "dateFrom": self._dt_string(date_from),
            "dateUntil": self._dt_string(date_to),
        }
        return self._call_api("w/user/ereignisse", query=query)

    def create_ereignis(self, zaehlpunkt, name, date_from, date_to=None):
        """Creates new event.

        Args:
            zaehlpunkt (str): Id for desired smartmeter.
                If None check for first meter in user profile
            name (str): Event name
            date_from (datetime.datetime): (Starting) date for request
            date_to (datetime.datetime, optional): Ending date for request.

        Returns:
            dict: JSON response of api call to 'w/user/ereignis'
        """
        if date_to is None:
            dto = None
            typ = "ZEITPUNKT"
        else:
            dto = self._dt_string(date_to)
            typ = "ZEITSPANNE"

        data = {
            "endAt": dto,
            "name": name,
            "startAt": self._dt_string(date_from),
            "typ": typ,
            "zaehlpunkt": zaehlpunkt,
        }

        return self._call_api("w/user/ereignis", data=data, method="POST")

    def delete_ereignis(self, ereignis_id):
        """Deletes ereignis."""
        return self._call_api("w/user/ereignis/{}".format(ereignis_id), method="DELETE")
