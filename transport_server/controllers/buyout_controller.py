import logging
import traceback

from transport_server.utils import get_db_connection

LOGGER = logging.getLogger(__name__)
handler = logging.StreamHandler()
formatter = logging.Formatter('[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s')
handler.setFormatter(formatter)
LOGGER.addHandler(handler)
LOGGER.setLevel(logging.INFO)


def buyout_booking(bookingId):  # noqa: E501
    """buyout_booking

     # noqa: E501

    :param bookingId: 
    :type bookingId: int

    :rtype: bool
    """
    sql = 'select "State" from "Sits" where "Booking_Id" = %s'
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(sql, (bookingId,))
            sit_state = cursor.fetchall()
    if sit_state:

        sql = 'update "Sits" ' \
              'set "State" = 3 where "Booking_Id" = %s '
        try:
            with get_db_connection() as connection:
                with connection.cursor() as cursor:
                    cursor.execute(sql, (bookingId,))
        except:
            LOGGER.error(traceback.format_exc())
            return False
        return True
    return False
