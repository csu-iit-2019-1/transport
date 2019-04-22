# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from transport_server.models.route import Route  # noqa: E501
from transport_server.models.prices import Prices  # noqa: E501
from transport_server.test import BaseTestCase


class TestTransportController(BaseTestCase):
    """TransportController integration test stubs"""

    def test_find_transport_by_parameters(self):
        """Test case for find_transport_by_parameters

        Finds transport by parameters
        """
        data = dict(points=56,
                    startPoint=789,
                    startDate=789,
                    endDate=789,
                    _class='coach',
                    countOfAdults=789,
                    countOfKids=789)
        response = self.client.open(
            '/CSU7/Transport/1.0.0/transport/get_list',
            method='POST',
            data=data,
            content_type='multipart/form-data')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_transport_by_id(self):
        """Test case for get_transport_by_id

        Find transport by ID
        """
        response = self.client.open(
            '/CSU7/Transport/1.0.0/transport/{transportId}'.format(transportId=789),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_getting_price_by_days(self):
        """Test case for getting_price_by_days

        
        """
        response = self.client.open(
            '/CSU7/Transport/1.0.0/transport/pricelist'.format(startDate=789, endDate=789, startPoint=789, endPoint=789),
            method='POST',
            content_type='multipart/form-data')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
