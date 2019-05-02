import json
import logging
from datetime import datetime

import traceback

from bottle import route, run, request, HTTPResponse

from booking_controller import book_transport
from buyout_controller import buyout_booking
from transport_controller import get_transport_by_id, \
    get_price_by_days

# from utils import psqlHandler

LOGGER = logging.getLogger(__name__)
# handler = psqlHandler({'host': "localhost", 'user': "postgres",
#                        'password': "secret", 'database': "Logs", 'port': '5639'})
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s %(message)s')
handler.setFormatter(formatter)
LOGGER.addHandler(handler)
LOGGER.setLevel(logging.INFO)

INVALID_INPUT = HTTPResponse(
    status=400,
    body=json.dumps('Invalid input')
)


@route('/transport/<transport_id>', method='GET')
def get_transport(transport_id):
    if not isinstance(transport_id, int) or transport_id < 1:
        return INVALID_INPUT

    data_to_response = get_transport_by_id(transport_id)
    if data_to_response:
        return HTTPResponse(
            status=200,
            body=json.dumps(data_to_response).encode('utf-8')
        )
    else:
        return HTTPResponse(
            status=400,
            body=json.dumps('Invalid operation').encode('utf-8')
        )


# @route('/transport/get_list', method='POST')
# def get_transport_list():
#     LOGGER.info('getting transport list')
#     try:
#         params = dict(request.json)
#     except:
#         LOGGER.error(traceback.format_exc())
#         return INVALID_INPUT
#     if not params:
#         LOGGER.info('No params')
#         return INVALID_INPUT
#     LOGGER.info('params: {}'.format(params))
#
#     start_point = params['startPoint']
#     end_points = params['endPoints']
#     departure_date = params['departureDate']
#     if 'countOfPersons' in params.keys():
#         count_of_persons = params['countOfPersons']
#     else:
#         count_of_persons = 0
#     if 'transportType' in params.keys():
#         transport_type = params['transportType']
#     else:
#         transport_type = ['aircraft', 'train', 'bus']
#
#     transport_list = find_transport_by_parameters(start_point, end_points, departure_date,
#                                                   count_of_persons, transport_type)
#     LOGGER.info(transport_list)
#     if transport_list:
#         return HTTPResponse(
#             status=200,
#             body=json.dumps(transport_list).encode('utf-8')
#         )
#     else:
#         return HTTPResponse(
#             status=400,
#             body='Invalid operation'
#         )


# @route('/logs', method='GET')
# def get_logs():
#     try:
#         with get_logs_connection


@route('/transport/pricelist', method='POST')
def get_pricelist():
    """
    :return: list of avg and min prices for types of transport by date
    """
    LOGGER.info('get list of cheap transport by day')
    required_params = [
        'departureDate',
        'startPoint',
        'endPoints',
        'transportType'
    ]
    try:
        params = dict(request.json)
    except:
        LOGGER.error(traceback.format_exc())
        return INVALID_INPUT

    for p in required_params:
        if p not in params.keys():
            return INVALID_INPUT
    departure_date = datetime.fromtimestamp(int(params['departureDate']))
    if datetime.today() >= departure_date:
        LOGGER.error('Date must after today')
        return HTTPResponse(
            status=400,
            body='Departure date must be grater then today'
        )
    departure_date = departure_date.strftime('%Y-%m-%d')
    count_of_persons = 0
    if 'countOfPersons' in params.keys() and isinstance(params['countOfPersons'], int):
        count_of_persons = params['countOfPersons']
    price_list = get_price_by_days(departure_date, params['startPoint'],
                                   params['endPoints'], params['transportType'], count_of_persons)
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
    try:
        transport_id = int(transport_id)
    except:
        LOGGER.info('invalid input of transport')
        return INVALID_INPUT

    required_params = [
        'personId',
        'countOfPersons'
    ]
    try:
        LOGGER.info(request.json)
        params = dict(request.json)
        LOGGER.info('{}, {}'.format(type(params), params))
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


@route('/transport/buyout/<booking_id>', method='GET')
def buy_booking(booking_id):
    LOGGER.info('buyouting for booking {}'.format(booking_id))
    try:
        booking_id = int(booking_id)
    except:
        LOGGER.info('invalid input of booking id')
        return HTTPResponse(
            status=200,
            body=json.dumps(False)
        )
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
