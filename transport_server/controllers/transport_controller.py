from transport_server.models.route import Route


def find_transport_by_parameters(params):
    """Finds transport by parameters

    :param points: 
    :type points: List[int]
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
    return 'do some magic!'


def get_transport_by_id(transportId):
    """Find transport by ID

    Returns a single transport # noqa: E501

    :param transportId: ID of transport
    :type transportId: int

    :rtype: Route
    """
    return 'do some magic!'


def getting_price_by_days(params):
    """getting_price_by_days

    :param startDate: 
    :type startDate: int
    :param endDate: 
    :type endDate: int
    :param startPoint: 
    :type startPoint: int
    :param endPoint: 
    :type endPoint: int

    :rtype: Dict
    """
    return 'do some magic!'
