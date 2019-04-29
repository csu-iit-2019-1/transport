from transport_server.models.buyout import Buyout  # noqa: E501
from transport_server.utils import get_db_connection


def buyout_booking(bookingId):  # noqa: E501
    """buyout_booking

     # noqa: E501

    :param bookingId: 
    :type bookingId: int

    :rtype: Buyout
    """

    sql = 'update "Sits" ' \
          'set "State" = 3 where "Booking_Id" = %s '
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(sql, (bookingId,))
    return Buyout(booking_id=bookingId, status='Success')
