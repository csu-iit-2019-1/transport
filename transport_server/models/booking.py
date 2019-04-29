# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from transport_server import util
from transport_server.models.base_model_ import Model


class Booking(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    # def __init__(self, booking_id: int=None, transport_id: int=None, person_id: int=None, count_of_adults: int=None, count_of_kids: int=None, price: float=None):  # noqa: E501
    def __init__(self, booking_id: int = None, transport_id: int = None, person_id: int = None, count_of_persons: int = None, price: float = None):  # noqa: E501
        """Booking - a model defined in Swagger

        :param booking_id: The booking_id of this Booking.  # noqa: E501
        :type booking_id: int
        :param transport_id: The transport_id of this Booking.  # noqa: E501
        :type transport_id: int
        :param person_id: The person_id of this Booking.  # noqa: E501
        :type person_id: int
        :param count_of_persons: The count_of_persons of this Booking.  # noqa: E501
        :type count_of_persons: int
        :param price: The price of this Booking.  # noqa: E501
        :type price: float
        """
        self.types = {
            'booking_id': int,
            'transport_id': int,
            'person_id': int,
            'count_of_persons': int,
            'price': float
        }

        self.attribute_map = {
            'booking_id': 'bookingId',
            'transport_id': 'transportId',
            'person_id': 'personId',
            'count_of_persons': 'countOfPersons',
            'price': 'price'
        }

        self._booking_id = booking_id
        self._transport_id = transport_id
        self._person_id = person_id
        self._count_of_persons = count_of_persons
        self._price = price

    @classmethod
    def from_dict(cls, dikt) -> 'Booking':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The Booking of this Booking.  # noqa: E501
        :rtype: Booking
        """
        return util.deserialize_model(dikt, cls)

    @property
    def booking_id(self) -> int:
        """Gets the booking_id of this Booking.


        :return: The booking_id of this Booking.
        :rtype: int
        """
        return self._booking_id

    @booking_id.setter
    def booking_id(self, booking_id: int):
        """Sets the booking_id of this Booking.


        :param booking_id: The booking_id of this Booking.
        :type booking_id: int
        """

        self._booking_id = booking_id

    @property
    def transport_id(self) -> int:
        """Gets the transport_id of this Booking.


        :return: The transport_id of this Booking.
        :rtype: int
        """
        return self._transport_id

    @transport_id.setter
    def transport_id(self, transport_id: int):
        """Sets the transport_id of this Booking.


        :param transport_id: The transport_id of this Booking.
        :type transport_id: int
        """
        if transport_id is None:
            raise ValueError("Invalid value for `transport_id`, must not be `None`")  # noqa: E501

        self._transport_id = transport_id

    @property
    def person_id(self) -> int:
        """Gets the person_id of this Booking.


        :return: The person_id of this Booking.
        :rtype: int
        """
        return self._person_id

    @person_id.setter
    def person_id(self, person_id: int):
        """Sets the person_id of this Booking.


        :param person_id: The person_id of this Booking.
        :type person_id: int
        """
        if person_id is None:
            raise ValueError("Invalid value for `person_id`, must not be `None`")  # noqa: E501

        self._person_id = person_id

    @property
    def count_of_persons(self) -> int:
        """Gets the count_of_persons of this Booking.


        :return: The count_of_persons of this Booking.
        :rtype: int
        """
        return self._count_of_persons

    @count_of_persons.setter
    def count_of_persons(self, count_of_persons: int):
        """Sets the count_of_persons of this Booking.


        :param count_of_persons: The count_of_persons of this Booking.
        :type count_of_persons: int
        """

        self._count_of_persons = count_of_persons

    @property
    def price(self) -> float:
        """Gets the price of this Booking.


        :return: The price of this Booking.
        :rtype: float
        """
        return self._price

    @price.setter
    def price(self, price: float):
        """Sets the price of this Booking.


        :param price: The price of this Booking.
        :type price: float
        """

        self._price = price
