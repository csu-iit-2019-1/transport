import json
import logging
import traceback

from bottle import route, run, request, response, HTTPResponse

from transport_server.controllers.booking_controller import book_transport
from transport_server.controllers.buyout_controller import buyout_booking
from transport_server.controllers.transport_controller import get_transport_by_id, find_transport_by_parameters, \
    getting_price_by_days

LOGGER = logging.getLogger(__name__)
handler = logging.StreamHandler()
formatter = logging.Formatter('[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s')
handler.setFormatter(formatter)
LOGGER.addHandler(handler)
LOGGER.setLevel(logging.INFO)

INVALID_INPUT = HTTPResponse(
    status=400,
    body=json.dumps('Invalid input')
)


@route('/transport/<transport_id>', method='GET')
def get_transport(transport_id):
    try:
        transport_id = int(transport_id)
        if transport_id <= 0:
            raise ValueError()
    except ValueError:
        LOGGER.error(traceback.format_exc())
        return INVALID_INPUT

    transport = get_transport_by_id(transport_id)
    if transport:
        return HTTPResponse(
            status=200,
            body=json.dumps(transport)
        )
    else:
        return HTTPResponse(
            status=404,
            body=json.dumps('Transport not found')
        )


@route('/transport/get_list', method='POST')
def get_transport_list():
    required_params = [
        'points',
        'startPoint',
        'startDate',
        'endDate',
        'countOfAdults'
    ]
    try:
        params = request.json
    except:
        LOGGER.error(traceback.format_exc())
        return INVALID_INPUT
    for p in required_params:
        if p not in params.keys:
            return INVALID_INPUT
    transport_list = find_transport_by_parameters(params)
    if transport_list:
        return HTTPResponse(
            status=200,
            body=json.dumps(transport_list)
        )
    else:
        return HTTPResponse(
            status=400,
            body='Invalid operation'
        )


@route('/transport/pricelist', method='POST')
def get_pricelist():
    """
    :return: list of avg and min prices for types of transport by date
    """
    required_params = [
        'startDate',
        'endDate',
        'startPoint',
        'endPoint'
    ]
    try:
        params = request.json
    except:
        LOGGER.error(traceback.format_exc())
        return INVALID_INPUT
    for p in required_params:
        if p not in params:
            return INVALID_INPUT
    price_list = getting_price_by_days(params)
    if price_list:
        return HTTPResponse(
            status=200,
            body=json.dumps(price_list)
        )
    else:
        return HTTPResponse(
            status=400,
            body='Invalid operation'
        )


@route('/transport/booking/<transport_id>', method='POST')
def booking_transport(transport_id):
    required_params = [
        'transportId',
        'personId',
        'countOfAdults'
    ]
    try:
        params = request.json
    except:
        LOGGER.error(traceback.format_exc())
        return INVALID_INPUT
    for p in required_params:
        if p not in params:
            return INVALID_INPUT
    booking = book_transport(transport_id, params)
    if booking:
        return HTTPResponse(
            status=200,
            body=json.dumps(booking)
        )
    else:
        return HTTPResponse(
            status=400,
            body=json.dumps('Invalid operation')
        )


@route('/transport/buyout/<booking_id>', method='POST')
def buy_booking(booking_id):
    buyout = buyout_booking(booking_id)
    if buyout:
        return HTTPResponse(
            status=200,
            body=json.dumps(buyout)
        )
    else:
        return HTTPResponse(
            status=400,
            body=json.dumps('Invalid operation')
        )
