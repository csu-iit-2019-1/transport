import json
import logging
import time
import traceback

import urllib3

from transport_server.models.sit import Sit
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


# def find_transport_by_parameters(start_point, end_points, departure_date, count_of_persons, transport_type,
#                                  search_cheap=False):
#     """Finds transport by parameters
#
#     :param endPoints:
#     :type endPoints: List[int]
#     :param startPoint:
#     :type startPoint: int
#     :param startDate:
#     :type startDate: int
#     :param transportType:
#     :type transportType: str
#     :param countOfAdults:
#     :type countOfAdults: int
#     :param countOfKids:
#     :type countOfKids: int
#
#     :rtype: List[Route]
#     """
#
#     LOGGER.info('method_params: {params}; {search_cheap}')
#
#     if 'points' in params.keys():
#         end_points = params['points']
#     elif 'endPoints' in params.keys():
#         end_points = params['endPoints']
#     else:
#         LOGGER.error('No end points')
#         return None
#
#     start_point = params['startPoint']
#
#     if 'startDate' in params.keys() and 'endDate' in params.keys():
#         try:
#             start_date = time.strptime(time.ctime(int(params['startDate'])), '%a %B %d %H:%M:%S %Y')
#             start_date = time.strftime('%Y-%m-%d', start_date)
#             end_date = time.strptime(time.ctime(int(params['endDate'])), '%a %B %d %H:%M:%S %Y')
#             end_date = time.strftime('%Y-%m-%d', end_date)
#         except ValueError:
#             LOGGER.error('Date must be integer')
#             return None
#         except:
#             LOGGER.error(traceback.format_exc())
#             return None
#     elif 'departureDate' in params.keys():
#         try:
#             start_date = time.strptime(time.ctime(int(params['departureDate'])), '%a %B %d %H:%M:%S %Y')
#             start_date = time.strftime('%Y-%m-%d', start_date)
#             end_date = start_date
#         except ValueError:
#             LOGGER.error('Date must be integer')
#             return None
#     else:
#         LOGGER.error('Invalid params of date')
#         return None
#
#     transport_type = ['airplane', 'bus', 'train']
#     if 'transportType' in params.keys():
#         transport_type = params['transportType']
#
#     end_cities = []
#
#     # try:
#     #     resp = http.request('GET', '/'.join([URL_CITY, start_point]))
#     #     start_city = resp.data.decode('utf-8')
#     # except:
#     #     LOGGER.error(traceback.format_exc())
#     #     return None
#     start_city = 'москва'
#     end_cities = {'челябинск': 1}
#
#     # for point in end_points:
#     # try:
#     #     resp = http.request('GET', '/'.join([URL_CITY, point]))
#     #     city = resp.data.decode('utf-8')
#     # except:
#     #     LOGGER.error(traceback.format_exc())
#     #     return None
#     # end_cities.append(city['name'])
#
#     sql_get_routes = 'select "Routes"."Id", "Types"."Name", "Routes"."Name", "Start_Point", "End_Point", ' \
#                      '"Departure_Time", "Arrive_Time", "Price", lower("Cities"."Name") ' \
#                      'from "Routes", "Types","Cities" ' \
#                      'where "Types"."Id" = "Routes"."Transport_Type"  and ' \
#                      '"Departure_Time"::date >= %s and "Departure_Time"::date <= %s ' \
#                      'and "Cities"."Id" = "Routes"."End_Point" and "Start_Point" = (' \
#                      'select "Id" from "Cities" where lower("Name") = %s) and "End_Point" in (' \
#                      'select "Id" from "Cities" where lower("Name") = %s '
#     for i in range(len(end_cities) - 1):
#         sql_get_routes += 'or lower("Name") = %s '
#     sql_get_routes += ') and (lower("Types"."Name") = %s '
#     for i in range(len(transport_type) - 1):
#         sql_get_routes += 'or lower("Types"."Name") = %s '
#     sql_get_routes += ')'
#
#     query_parameters = [start_date, end_date, start_city] + [x for x in end_cities.keys()] + transport_type
#
#     # if search_cheap:
#     #     sql_get_routes += 'and "Price" = (select min("Price") from "Routes", "Types" ' \
#     #                       'where "Types"."Id" = "Routes"."Transport_Type" ' \
#     #                       'and "Departure_Time"::date >= %s and "Departure_Time"::date <= %s ' \
#     #                       'and "Types"."Name" = %s '
#     #     for i in range(len(transport_type) - 1):
#     #         sql_get_routes += 'or lower("Transport_Type") like (%s) '
#     #     sql_get_routes += ')'
#     #     query_parameters += [start_date, end_date] + transport_type
#
#     with get_db_connection() as connection:
#         with connection.cursor() as cursor:
#             cursor.execute(sql_get_routes, tuple(query_parameters))
#             routes_data = cursor.fetchall()
#
#     routes = []
#     routes_train = None
#     routes_bus = None
#     routes_airplane = None
#     if not search_cheap:
#         for route in routes_data:
#             routes.append(Route(transport_id=route[0],
#                                 transport_type=route[1],
#                                 name=route[2],
#                                 start_point=start_point,
#                                 end_point=end_cities[route[8]],
#                                 departure_time=int(route[5].timestamp()),
#                                 arrive_time=int(route[6].timestamp()),
#                                 price=route[7],
#                                 sits=None))
#     else:
#         for route in routes_data:
#             if route[1] == 'train':
#                 if not routes_train or route[7] < routes_train.price:
#                     routes_train = Route(transport_id=route[0],
#                                          transport_type=route[1],
#                                          name=route[2],
#                                          start_point=start_point,
#                                          end_point=end_cities[route[8]],
#                                          departure_time=int(route[5].timestamp()),
#                                          arrive_time=int(route[6].timestamp()),
#                                          price=route[7],
#                                          sits=None)
#             elif route[1] == 'bus':
#                 if not routes_bus or route[7] < routes_bus.price:
#                     routes_bus = Route(transport_id=route[0],
#                                        transport_type=route[1],
#                                        name=route[2],
#                                        start_point=start_point,
#                                        end_point=end_cities[route[8]],
#                                        departure_time=int(route[5].timestamp()),
#                                        arrive_time=int(route[6].timestamp()),
#                                        price=route[7],
#                                        sits=None)
#             elif route[1] == 'airplane':
#                 if not routes_airplane or route[7] < routes_airplane.price:
#                     routes_airplane = Route(transport_id=route[0],
#                                             transport_type=route[1],
#                                             name=route[2],
#                                             start_point=start_point,
#                                             end_point=end_cities[route[8]],
#                                             departure_time=int(route[5].timestamp()),
#                                             arrive_time=int(route[6].timestamp()),
#                                             price=route[7],
#                                             sits=None)
#             routes = []
#             if routes_bus:
#                 routes.append(routes_bus)
#             if routes_airplane:
#                 routes.append(routes_airplane)
#             if routes_train:
#                 routes.append(routes_train)
#     res = []
#     for r in routes:
#         res.append(r.to_dict())
#     return res


def get_transport_by_id(transport_id):
    """Find transport by ID

    Returns a single transport # noqa: E501

    :param transportId: ID of transport
    :type transportId: int

    :rtype: Route
    """
    sql_get_transport = 'select "Routes"."Id", "Types"."Name", "Routes"."Name", ' \
                        '"Start_Point", "End_Point", "Departure_Time", "Arrive_Time", "Price" ' \
                        'from "Routes", "Types" ' \
                        'where "Routes"."Id" = %s and "Routes"."Transport_Type" = "Types"."Id";'
    sql_get_cities = 'select lower("Name") from "Cities" where "Id" = %s or "Id" = %s'
    sql_get_sits = 'select "Transport_Id", "State", "Sit_Number" ' \
                   'from "Sits" where "Transport_Id" = %s'

    try:
        with get_db_connection() as connecton:
            with connecton.cursor() as cursor:
                cursor.execute(sql_get_transport, (transport_id,))
                route_data = cursor.fetchone()
                if not route_data:
                    LOGGER.error('Route not found')
                    return None
                cursor.execute(sql_get_cities, (route_data[3], route_data[4]))
                cities = cursor.fetchall()
                if not cities or len(cities) < 2:
                    LOGGER.error('Cities not found')
                    return None
                cursor.execute(sql_get_sits, (transport_id,))
                sits = cursor.fetchall()
                if not sits:
                    LOGGER.error('Sits not found')
                    return None
    except:
        LOGGER.error(traceback.format_exc())
        return None

    start_city = cities[0][0]
    end_city = cities[0][0]
    start_point = route_data[3]
    end_point = route_data[4]
    # try:
    #     resp = http.request('GET', '/'.join([URL_CITY, start_city.title(), 'cityid']))
    #     start_city = json.loads(resp.data)
    #     if start_city and isinstance(start_city, list):
    #         start_point = start_city[0]['cityId']
    #     else:
    #         raise Exception
    #     resp = http.request('GET', '/'.join([URL_CITY, end_city.title(), 'cityid']))
    #     end_city = json.loads(resp.data)
    #     if end_city and isinstance(end_city, list):
    #         end_point = end_city[0]['cityId']
    #     else:
    #         raise Exception
    # except:
    #     LOGGER.error(traceback.format_exc())
    #     return None

    sits_list = []
    for sit in sits:
        sits_list.append(Sit(state=sit[1],
                             sit_number=sit[2]))

    route = Route(transport_id=transport_id,
                  transport_type=route_data[1],
                  name=route_data[2],
                  start_point=start_point,
                  end_point=end_point,
                  departure_time=int(route_data[5].timestamp()),
                  arrive_time=int(route_data[6].timestamp()),
                  price=route_data[7],
                  sits=sits_list)
    return route.to_dict()


def get_price_by_days(departure_date, start_point, end_points, transport_type, count_of_persons):
    start_city_name = start_point
    # try:
    #     res = http.request('GET', 'city/{}'.format(start_point))
    #     start_city = json.loads(res)
    #     if start_city:
    #         start_city_name = start_city['name'].lower()
    #     else:
    #         LOGGER.error('no city with such id')
    #         return None
    # except:
    #     LOGGER.error(traceback.format_exc())
    #     return None
    # end_city_names = {}
    # for point in end_points:
    #     try:
    #         res = http.request('GET', 'city/{}'.format(point))
    #         end_city = json.loads(res)
    #         if end_city:
    #             end_city_names[end_city['name'].lower()] = point
    #         else:
    #             LOGGER.error('no city with such id')
    #             return None
    #     except:
    #         LOGGER.error(traceback.format_exc())
    #         return None
    end_city_names = {}
    for c in end_points:
        end_city_names[c] = c

    sql_select_start_point = 'select "Id" from "Cities" ' \
                             'where lower("Name") = %s'
    sql_select_end_points = 'select "Id", lower("Name") from "Cities" ' \
                            'where lower("Name") = %s '
    for i in range(len(end_city_names) - 1):
        sql_select_end_points += 'or lower("Name") = %s'
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(sql_select_start_point, (start_city_name,))
            start_point_id = cursor.fetchone()[0]
            if not start_point:
                LOGGER.error('No such city in db')
                return None
            cursor.execute(sql_select_end_points, [k for k in end_city_names.keys()])
            end_points_data = cursor.fetchall()
            if not end_points_data:
                LOGGER.error('No such cities in db')
    sql_get_routes_by_end_point = 'select "Routes"."Id", "Routes"."Name", ' \
                                  '"Departure_Time", "Arrive_Time", "Price" ' \
                                  'from "Routes", "Types" ' \
                                  'where "Start_Point" = %s and "End_Point" = %s ' \
                                  'and "Types"."Id" = "Routes"."Transport_Type" ' \
                                  'and "Departure_Time"::date >= %s and "Departure_Time"::date <= %s ' \
                                  'and "Types"."Name" = %s and "Price" = (' \
                                  'select min("Price") from "Routes", "Types" ' \
                                  'where "Start_Point" = %s and "End_Point" = %s ' \
                                  'and "Types"."Id" = "Routes"."Transport_Type" ' \
                                  'and "Departure_Time"::date >= %s and "Departure_Time"::date <= %s ' \
                                  'and "Types"."Name" = %s)'
    routes_resp = []
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            for p in end_points_data:
                for t_type in transport_type:
                    query_params = [start_point_id, p[0], departure_date, departure_date, t_type]
                    cursor.execute(sql_get_routes_by_end_point, query_params + query_params)
                    route_data = cursor.fetchone()
                    if route_data:
                        routes_resp.append(Route(transport_id=route_data[0],
                                                 transport_type=t_type,
                                                 name=route_data[1],
                                                 start_point=start_point,
                                                 end_point=end_city_names[p[1]],
                                                 departure_time=int(route_data[2].timestamp()),
                                                 arrive_time=int(route_data[3].timestamp()),
                                                 price=route_data[4],
                                                 sits=None).to_dict())
                    else:
                        routes_resp.append(Route(transport_id=-1,
                                                 start_point=start_point,
                                                 end_point=end_city_names[p[1]],
                                                 transport_type=t_type))
    return routes_resp


# tr = get_price_by_days('2019-05-05', 'москва', ['париж', 'лондон'], ['aircraft', 'train'], 0)
# for t in tr:
#     print(t)
