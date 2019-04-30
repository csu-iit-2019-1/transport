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

    LOGGER.info(f'method_params: {params}; {search_cheap}')

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
            start_date = time.strptime(time.ctime(int(params['departureDate'])), '%a %B %d %H:%M:%S %Y')
            start_date = time.strftime('%Y-%m-%d', start_date)
            end_date = start_date
        except ValueError:
            LOGGER.error('Date must be integer')
            return None
    else:
        LOGGER.error('Invalid params of date')
        return None

    transport_type = ['airplane', 'bus', 'train']
    if 'transportType' in params.keys():
        transport_type = params['transportType']

    end_cities = []

    # try:
    #     resp = http.request('GET', '/'.join([URL_CITY, start_point]))
    #     start_city = resp.data.decode('utf-8')
    # except:
    #     LOGGER.error(traceback.format_exc())
    #     return None
    start_city = 'москва'
    end_cities = {'челябинск': 1}

    # for point in end_points:
    # try:
    #     resp = http.request('GET', '/'.join([URL_CITY, point]))
    #     city = resp.data.decode('utf-8')
    # except:
    #     LOGGER.error(traceback.format_exc())
    #     return None
    # end_cities.append(city['name'])

    sql_get_routes = 'select "Routes"."Id", "Types"."Name", "Routes"."Name", "Start_Point", "End_Point", ' \
                     '"Departure_Time", "Arrive_Time", "Price", lower("Cities"."Name") ' \
                     'from "Routes", "Types","Cities" ' \
                     'where "Types"."Id" = "Routes"."Transport_Type"  and ' \
                     '"Departure_Time"::date >= %s and "Departure_Time"::date <= %s ' \
                     'and "Cities"."Id" = "Routes"."End_Point" and "Start_Point" = (' \
                     'select "Id" from "Cities" where lower("Name") = %s) and "End_Point" in (' \
                     'select "Id" from "Cities" where lower("Name") = %s '
    for i in range(len(end_cities) - 1):
        sql_get_routes += 'or lower("Name") = %s '
    sql_get_routes += ') and (lower("Types"."Name") = %s '
    for i in range(len(transport_type) - 1):
        sql_get_routes += 'or lower("Types"."Name") = %s '
    sql_get_routes += ')'

    query_parameters = [start_date, end_date, start_city] + [x for x in end_cities.keys()] + transport_type

    # if search_cheap:
    #     sql_get_routes += 'and "Price" = (select min("Price") from "Routes", "Types" ' \
    #                       'where "Types"."Id" = "Routes"."Transport_Type" ' \
    #                       'and "Departure_Time"::date >= %s and "Departure_Time"::date <= %s ' \
    #                       'and "Types"."Name" = %s '
    #     for i in range(len(transport_type) - 1):
    #         sql_get_routes += 'or lower("Transport_Type") like (%s) '
    #     sql_get_routes += ')'
    #     query_parameters += [start_date, end_date] + transport_type

    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(sql_get_routes, tuple(query_parameters))
            routes_data = cursor.fetchall()

    routes = []
    routes_train = None
    routes_bus = None
    routes_airplane = None
    if not search_cheap:
        for route in routes_data:
            routes.append(Route(transport_id=route[0],
                                transport_type=route[1],
                                name=route[2],
                                start_point=start_point,
                                end_point=end_cities[route[8]],
                                departure_time=int(route[5].timestamp()),
                                arrive_time=int(route[6].timestamp()),
                                price=route[7],
                                sits=None))
    else:
        for route in routes_data:
            if route[1] == 'train':
                if not routes_train or route[7] < routes_train.price:
                    routes_train = Route(transport_id=route[0],
                                         transport_type=route[1],
                                         name=route[2],
                                         start_point=start_point,
                                         end_point=end_cities[route[8]],
                                         departure_time=int(route[5].timestamp()),
                                         arrive_time=int(route[6].timestamp()),
                                         price=route[7],
                                         sits=None)
            elif route[1] == 'bus':
                if not routes_bus or route[7] < routes_bus.price:
                    routes_bus = Route(transport_id=route[0],
                                       transport_type=route[1],
                                       name=route[2],
                                       start_point=start_point,
                                       end_point=end_cities[route[8]],
                                       departure_time=int(route[5].timestamp()),
                                       arrive_time=int(route[6].timestamp()),
                                       price=route[7],
                                       sits=None)
            elif route[1] == 'airplane':
                if not routes_airplane or route[7] < routes_airplane.price:
                    routes_airplane = Route(transport_id=route[0],
                                            transport_type=route[1],
                                            name=route[2],
                                            start_point=start_point,
                                            end_point=end_cities[route[8]],
                                            departure_time=int(route[5].timestamp()),
                                            arrive_time=int(route[6].timestamp()),
                                            price=route[7],
                                            sits=None)
            routes = []
            if routes_bus:
                routes.append(routes_bus)
            if routes_airplane:
                routes.append(routes_airplane)
            if routes_train:
                routes.append(routes_train)
    res = []
    for r in routes:
        res.append(r.to_dict())
    return res


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
    LOGGER.info(transport_id)

    sql_get_transport = 'select "Routes"."Id", "Types"."Name", "Routes"."Name", ' \
                        '"Start_Point", "End_Point", "Departure_Time", "Arrive_Time", "Price" ' \
                        'from "Routes", "Types" ' \
                        'where "Routes"."Id" = %s and "Routes"."Transport_Type" = "Types"."Id";'
    sql_get_cities = 'select lower("Name") from "Cities" where "Id" = %s or "Id" = %s'
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

    # start_city = cities[0][0]
    # try:
    #     resp = http.request('GET', '/'.join([URL_CITY, start_city]))
    #     start_city = resp.data.decode('utf-8')
    # except:
    #     LOGGER.error(traceback.format_exc())
    #     return None
    # end_city = cities[0][0]
    # try:
    #     resp = http.request('GET', '/'.join([URL_CITY, start_city]))
    #     end_city = resp.data.decode('utf-8')
    # except:
    #     LOGGER.error(traceback.format_exc())
    #     return None

    sits_list = []
    for sit in sits:
        sits_list.append(Sit(transport_id=transport_id,
                             state=sit[1],
                             sit_number=sit[2]))

    route = Route(transport_id=transport_id,
                  transport_type=route_data[1],
                  name=route_data[2],
                  start_point=route_data[3],
                  end_point=route_data[4],
                  departure_time=int(route_data[5].timestamp()),
                  arrive_time=int(route_data[6].timestamp()),
                  price=route_data[7],
                  sits=sits_list)
    return route.to_dict()


def get_price_by_days(params):
    """getting_price_by_days

    :param departureDate:
    :type departureDate: int
    :param startPoint:
    :type startPoint: int
    :param endPoints:
    :type endPoints: List[int]

    :rtype: List[Route]
    """
    LOGGER.info(params)
    return find_transport_by_parameters(params, search_cheap=True)
    # res =[]
    # for r in tr:
    #     res.append(r.to_dict())
    # return res


pp = find_transport_by_parameters({
    'departureDate': 1556811480,
    'transportType': ['airplane', 'bus'],
    'startPoint': 1,
    'endPoints': [10]
})
for p in pp:
    print(p)
