import logging
import time
import traceback

import urllib3

from transport_server.models import Sit
from transport_server.models.route import Route
from transport_server.utils import get_db_connection

LOGGER = logging.getLogger(__name__)
handler = logging.StreamHandler()
formatter = logging.Formatter('[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s')
handler.setFormatter(formatter)
LOGGER.addHandler(handler)
LOGGER.setLevel(logging.INFO)

http = urllib3.PoolManager()

URL_CITY = 'localhost/city'


def find_transport_by_parameters(params, search_cheap=False):
    """Finds transport by parameters

    :param endPoints:
    :type endPoints: List[int]
    :param startPoint: 
    :type startPoint: int
    :param startDate: 
    :type startDate: int
    :param endDate: 
    :type endDate: int
    :param transportType:
    :type transportType: str
    :param _class: 
    :type _class: List[str]
    :param countOfAdults: 
    :type countOfAdults: int
    :param countOfKids: 
    :type countOfKids: int

    :rtype: List[Route]
    """

    if 'points' in params.keys():
        end_points = params['points']
    elif 'endPoints' in params.keys():
        end_points = params['endPoints']
    else:
        LOGGER.error('No end points')
        return None

    start_point = params['startPoint']

    if 'startDate' in params.keys() and 'endDate' in params.keys():
        try:
            start_date = time.strptime(time.ctime(int(params['startDate'])), '%a %B %d %H:%M:%S %Y')
            start_date = time.strftime('%Y-%m-%d', start_date)
            end_date = time.strptime(time.ctime(int(params['endDate'])), '%a %B %d %H:%M:%S %Y')
            end_date = time.strftime('%Y-%m-%d', end_date)
        except ValueError:
            LOGGER.error('Date must be integer')
            return None
        except:
            LOGGER.error(traceback.format_exc())
            return None
    elif 'departureDate' in params.keys():
        try:
            start_date = time.strptime(time.ctime(int(params['date'])), '%a %B %d %H:%M:%S %Y')
            start_date = time.strftime('%Y-%m-%d', start_date)
            end_date = start_date
        except ValueError:
            LOGGER.error('Date must be integer')
            return None
    else:
        LOGGER.error('Invalid params of date')
        return None

    transport_type = None
    if 'transportType' in params.keys():
        transport_type = params['transportType']

    end_cities = []

    try:
        resp = http.request('GET', '/'.join([URL_CITY, start_point]))
        start_city = resp.data.decode('utf-8')
    except:
        LOGGER.error(traceback.format_exc())
        return None

    for point in end_points:
        try:
            resp = http.request('GET', '/'.join([URL_CITY, point]))
            city = resp.data.decode('utf-8')
        except:
            LOGGER.error(traceback.format_exc())
            return None
        end_cities.append(city['name'])

    sql_get_routes = 'select "Routes"."Id", "Types"."Name", "Routes"."Name", "Start_Point", "End_Point", ' \
                     '"Departure_Time", "Arrive_Time", "Price", "Cities"."Name" as end_point ' \
                     'from "Routes", "Types", "Cities" ' \
                     'where "Types"."Id" = "Routes"."Transport_Type" and ' \
                     '"Departure_Time"::date >= %s and "Departure_Time"::date <= %s ' \
                     'and "End_Point" = "Cities"."Id" and "Start_Point" = (' \
                     'select "Id" from "Cities" where lower("Name") like (%s)) and "End_Point" in (' \
                     'select "Id" from "Cities" where lower("name") like(%s) '
    for i in range(len(end_cities) - 1):
        sql_get_routes += 'or lower("name") like (%s) '
    sql_get_routes += ') '

    query_parameters = [start_date, end_date, start_city] + end_cities

    if transport_type:
        sql_get_routes += ' and lower("Types"."Name") like(%s) '
        query_parameters.append(transport_type)

    if search_cheap:
        sql_get_routes += ' group by "Routes"."Id", "Types"."Name", "Routes"."Name", "Start_Point", "End_Point", ' \
                          '"Departure_Time", "Arrive_Time", "Cities"."Name" ' \
                          'having "Price" = min("Price")'

    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(sql_get_routes, tuple(query_parameters))
            routes_data = cursor.fetchall()

    routes = []
    for route in routes_data:
        routes.append(Route(transport_id=route[0],
                            transport_type=route[1],
                            name=route[2],
                            start_point=route[3],
                            end_point=route[8],
                            departure_time=int(route[5].timestamp()),
                            arrive_time=int(route[6].timestamp()),
                            price=route[7],
                            sits=[]))

    return routes


def get_transport_by_id(transport_id):
    """Find transport by ID

    Returns a single transport # noqa: E501

    :param transportId: ID of transport
    :type transportId: int

    :rtype: Route
    """
    if not isinstance(transport_id, int):
        try:
            transport_id = int(transport_id)
        except ValueError:
            LOGGER.error('transport id must be positive integer')
            return None
    if transport_id <= 0:
        LOGGER.error('transport id must be positive integer')
        return None

    sql_get_transport = 'select "Routes"."Id", "Types"."Name", "Routes"."Name", ' \
                        '"Start_Point", "End_Point", "Departure_Time", "Arrive_Time", "Price" ' \
                        'from "Routes", "Types" ' \
                        'where "Routes"."Id" = %s and "Routes"."Transport_Type" = "Types"."Id";'
    sql_get_cities = 'select "Name" from "Cities" where "Id" = %s or "Id" = %s'
    sql_get_sits = 'select "Transport_Id", "State", "Sit_Number" ' \
                   'from "Sits" where "Transport_Id" = %s'
    with get_db_connection() as connecton:
        with connecton.cursor() as cursor:
            cursor.execute(sql_get_transport, (transport_id,))
            route_data = cursor.fetchone()
            cursor.execute(sql_get_cities, (route_data[3], route_data[4]))
            cities = cursor.fetchall()
            cursor.execute(sql_get_sits, (transport_id,))
            sits = cursor.fetchall()

    sits_list = []
    for sit in sits:
        sits_list.append(Sit(transport_id=transport_id,
                             state=sit[1],
                             sit_number=sit[2]))

    route = Route(transport_id=transport_id,
                  transport_type=route_data[1],
                  name=route_data[2],
                  start_point=cities[0][0],
                  end_point=cities[1][0],
                  departure_time=int(route_data[5].timestamp()),
                  arrive_time=int(route_data[6].timestamp()),
                  price=route_data[7],
                  sits=sits_list)
    print(route.to_str())
    return route


def getting_price_by_days(params):
    """getting_price_by_days

    :param departureDate:
    :type departureDate: int
    :param startPoint:
    :type startPoint: int
    :param endPoints:
    :type endPoints: List[int]

    :rtype: List[Route]
    """
    return find_transport_by_parameters(params, search_cheap=True)
