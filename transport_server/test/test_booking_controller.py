# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from transport_server.models.booking import Booking  # noqa: E501
from transport_server.test import BaseTestCase


class TestBookingController(BaseTestCase):
    """BookingController integration test stubs"""

    def test_booking_transport(self):
        """Test case for booking_transport

        
        """
        data = dict(personId=56,
                    countOfAdults=789,
                    countOfKids=789)
        response = self.client.open(
            '/CSU7/Transport/1.0.0/transport/booking/{transportId}'.format(transportId=789),
            method='POST',
            data=data,
            content_type='multipart/form-data')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
