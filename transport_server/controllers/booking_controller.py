import logging

from transport_server.models.booking import Booking
from transport_server.utils import get_db_connection

LOGGER = logging.getLogger(__name__)
handler = logging.StreamHandler()
formatter = logging.Formatter('[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s')
handler.setFormatter(formatter)
LOGGER.addHandler(handler)
LOGGER.setLevel(logging.INFO)


def book_transport(transport_id, params):  # noqa: E501
    """booking_transport

    :param transportId: 
    :type transportId: int
    :param personId: 
    :type personId: int
    :param countOfPersons:
    :type countOfPersons: int

    :rtype: Booking
    """
    person_id = params['personId']
    count_of_persons = int(params['countOdPersons'])

    sql = 'select "Id" from "Sits" ' \
          'where "Transport_Id" = %s and "State" = 1'
    sql_get_price = 'select "Price" from "Routes" where "Id" = %s'
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(sql, (transport_id,))
            sits_data = cursor.fetchall()
            cursor.execute(sql_get_price, (transport_id,))
            price = cursor.fetchone()[0]

    if len(sits_data) < count_of_persons:
        LOGGER.error('No available sits')
        return None

    sits_id = [x[0] for x in sits_data]
    sits_to_book = sits_id[:count_of_persons]

    sql = 'update "Sits" ' \
          'set "State" = 2, "Person_Id" = %s where "Id" = %s '
    if count_of_persons > 1:
        sql += 'or "Id" = %s'

    query_params = [person_id] + sits_to_book

    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(sql, tuple(query_params))

    return Booking(booking_id=sits_to_book[0],
                   transport_id=transport_id,
                   person_id=person_id,
                   count_of_persons=count_of_persons,
                   price=price)
