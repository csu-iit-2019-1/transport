import logging
import traceback

from utils import get_db_connection, psqlHandler

LOGGER = logging.getLogger(__name__)
handler = psqlHandler({'host': "localhost", 'user': "postgres",
                       'password': "secret", 'database': "Logs", 'port': '5639'})
formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s %(message)s')
handler.setFormatter(formatter)
LOGGER.addHandler(handler)
LOGGER.setLevel(logging.INFO)


def book_transport(transport_id, person_id, count_of_persons):  # noqa: E501
    """booking_transport

    :param transportId: 
    :type transportId: int
    :param personId: 
    :type personId: int
    :param countOfPersons:
    :type countOfPersons: int

    :rtype: dict
    """
    LOGGER.info('booking starts!!!!')

    sql = 'select "Id" from "Sits" ' \
          'where "Transport_Id" = %s and "State" = 1'
    sql_get_price = 'select "Price" from "Routes" where "Id" = %s'
    try:
        with get_db_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(sql, (transport_id,))
                sits_data = cursor.fetchall()
                if not sits_data or len(sits_data) < count_of_persons:
                    return 'No available sits'

                cursor.execute(sql_get_price, (transport_id,))
                price = cursor.fetchone()[0]
    except:
        LOGGER.error(traceback.format_exc())
        print(traceback.format_exc())
        return None

    LOGGER.info('count of available sits: {}'.format(len(sits_data)))

    sits_id_available = [x[0] for x in sits_data]
    sits_to_book = sits_id_available[:count_of_persons]

    sql_insert_booking = 'insert into "Booking_Info"("Person_Id", "Transport_Id", "Count_Of_Persons", "Price") ' \
                         'values (%s, %s, %s, %s)'
    sql_select_booking_id = 'select "Id" from "Booking_Info" ' \
                            'where "Person_Id" = %s and "Transport_Id" = %s'
    try:
        with get_db_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(sql_insert_booking, (person_id, transport_id, count_of_persons, price*count_of_persons))
                cursor.execute(sql_select_booking_id, (person_id, transport_id))
                booking_id = cursor.fetchone()[0]
    except:
        LOGGER.error(traceback.format_exc())
        print(traceback.format_exc())
        return 'Booking failed'

    sql = 'update "Sits" ' \
          'set "State" = 2, "Booking_Id" = %s where "Id" = %s '
    for i in range(count_of_persons - 1):
        sql += 'or "Id" = %s '

    query_params = [booking_id] + sits_to_book

    try:
        with get_db_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(sql, query_params)
    except:
        LOGGER.error(traceback.format_exc())
        print(traceback.format_exc())
        return 'Booking failed'

    return {'bookingId': booking_id}


print(book_transport(1, 1, 1))
