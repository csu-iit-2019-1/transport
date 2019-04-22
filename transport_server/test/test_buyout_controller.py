# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from transport_server.models.buyout import Buyout  # noqa: E501
from transport_server.test import BaseTestCase


class TestBuyoutController(BaseTestCase):
    """BuyoutController integration test stubs"""

    def test_buyout_booking(self):
        """Test case for buyout_booking

        
        """
        response = self.client.open(
            '/CSU7/Transport/1.0.0/transport/buyout/{bookingId}'.format(bookingId=789),
            method='POST',
            content_type='mulipart/form-data')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
