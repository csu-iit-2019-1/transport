import json
import logging
import time
import gunicorn
import traceback

from bottle import route, run, request, response, HTTPResponse

from transport_server.controllers.booking_controller import book_transport
from transport_server.controllers.buyout_controller import buyout_booking
from transport_server.controllers.transport_controller import get_transport_by_id, find_transport_by_parameters, \
    get_price_by_days

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
    LOGGER.info('==========request!!===========')
    LOGGER.info(transport_id)
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
            body=json.dumps(transport).encode('utf-8')
        )
    else:
        return HTTPResponse(
            status=404,
            body=json.dumps('Transport not found').encode('utf-8')
        )


@route('/transport/get_list', method='POST')
def get_transport_list():
    try:
        params = dict(request.json)
        if not params:
            params = {
                'departureDate': request.forms.get('departureDate'),
                'transportType': request.forms.get('transportType'),
                'startPoint': request.forms.get('startPoint'),
                'endPoints': request.forms.get('endPoints')
            }
        LOGGER.info(f'{type(params)}, {params}')
    except:
        LOGGER.error(traceback.format_exc())
        return INVALID_INPUT
    if not params:
        LOGGER.info('No params')
        return INVALID_INPUT

    transport_list = find_transport_by_parameters(params)
    LOGGER.info(transport_list)
    if transport_list:
        return HTTPResponse(
            status=200,
            body=json.dumps(transport_list).encode('utf-8')
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
        'departureDate',
        'startPoint',
        'endPoints'
    ]
    try:
        params = dict(request.json)
        if not params:
            params = {
                'departureDate': request.forms.get('departureDate'),
                'transportType': request.forms.get('transportType'),
                'startPoint': request.forms.get('startPoint'),
                'endPoints': request.forms.get('endPoints')
            }
        LOGGER.info(f'{type(params)}, {params}')
    except:
        LOGGER.error(traceback.format_exc())
        return INVALID_INPUT
    if not params:
        LOGGER.info('No params')
        return INVALID_INPUT

    for p in required_params:
        if p not in params:
            return INVALID_INPUT
    price_list = get_price_by_days(params)
    LOGGER.info(price_list)
    if price_list:
        return HTTPResponse(
            status=200,
            body=json.dumps(price_list).encode('utf-8')
        )
    else:
        return HTTPResponse(
            status=400,
            body='Invalid operation'
        )


@route('/transport/booking/<transport_id>', method='POST')
def booking_transport(transport_id):
    LOGGER.info('book for transport {}'.format(transport_id))
    if not isinstance(transport_id, int) or transport_id < 1:
        return INVALID_INPUT

    required_params = [
        'personId',
        'countOfPersons'
    ]
    try:
        params = dict(request.json)
        LOGGER.info(f'{type(params)}, {params}')
    except:
        LOGGER.error(traceback.format_exc())
        return INVALID_INPUT
    for p in required_params:
        if p not in params or not isinstance(params[p], int):
            return INVALID_INPUT
    LOGGER.info('book params: {}', params)

    date_to_response = book_transport(transport_id, params['personId'], params['countOfPersons'])
    LOGGER.info('book response: {}'.format(date_to_response))

    if date_to_response:
        if isinstance(date_to_response, dict):
            return HTTPResponse(
                status=200,
                body=json.dumps(date_to_response).encode('utf-8')
            )
        else:
            date_to_response = 'Invalid operation'
    return HTTPResponse(
        status=400,
        body=json.dumps(date_to_response)
    )


@route('/transport/buyout/<booking_id>', method='POST')
def buy_booking(booking_id):
    if not isinstance(booking_id, int) or booking_id < 1:
        return INVALID_INPUT
    buyout_result = buyout_booking(booking_id)
    LOGGER.info('buyout result: {}'.format(buyout_result))
    return HTTPResponse(
        status=200,
        body=json.dumps(buyout_result)
    )


if __name__ == '__main__':
    LOGGER.info("SERVER HAS BEEN STARTED!!!")
    # run(host='0.0.0.0', port=8080)
    run(host='0.0.0.0', port=8181, server='gunicorn', workers=4, reload=True, debug=False)
