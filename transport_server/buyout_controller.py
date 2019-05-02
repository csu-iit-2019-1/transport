import logging
import traceback

from utils import get_db_connection

LOGGER = logging.getLogger(__name__)
# handler = psqlHandler({'host': "localhost", 'user': "postgres",
#                        'password': "secret", 'database': "Logs", 'port': '5639'})
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s %(message)s')
handler.setFormatter(formatter)
LOGGER.addHandler(handler)
LOGGER.setLevel(logging.INFO)


def buyout_booking(bookingId):
    """buyout_booking

     # noqa: E501

    :param bookingId: 
    :type bookingId: int

    :rtype: bool
    """
    sql_select_booking = 'select * from "Booking_Info" where "Id" = %s and "Status" = 0'

    sql_update_booking_status = 'update "Booking_Info" ' \
                                'set "Status" = 1 where "Id" = %s '
    # sql_insert_booking = 'insert into "Booking_Info"("Person_Id", "Transport_Id", "Count_Of_Persons", "Price") ' \
    #                      'values (%s, %s, %s, %s)
    try:
        with get_db_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(sql_select_booking, (bookingId,))
                booking = cursor.fetchone()
                if not booking:
                    LOGGER.error('Booking not found')
                    return False
                cursor.execute(sql_update_booking_status, (bookingId,))
    except:
        LOGGER.info(traceback.format_exc())
        print(traceback.format_exc())
        return False
    return True


print(buyout_booking(1))
