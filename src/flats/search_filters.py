"""
Модуль содержит фильтры поиска для роутеров.

Если необходимо изменить фильтр, то добавляем новый аргумент функции,
название которого соответствует свойству (атрибуту) модели из файла models.py
или удаляем ненужный аргумент.

Больше изменений в коде не потребуется, остальное сработает автоматически.
"""


def project_filters(
        project_id: int | None = None,
        city: str | None = None,
        name: str | None = None,
        metro: str | None = None
) -> dict[str: int | str]:
    """
    Фильтры для поиска ЖК.

    :param project_id: id ЖК;
    :param city: название города в котором находится ЖК;
    :param name: название ЖК;
    :param metro: ближайшее метро;
    :return: словарь с параметрами поиска.
    """
    result_filter = dict()
    if project_id:
        result_filter['project_id'] = project_id
    if city:
        result_filter['city'] = city
    if name:
        result_filter['name'] = name
    if metro:
        result_filter['metro'] = metro
    return result_filter


def flat_filters(
        flat_id: int | None = None,
        project_id: int | None = None,
        floor: int | None = None,
        rooms: int | None = None,
        area: float | None = None,
        finishing: str | None = None
) -> dict[str: int | str]:
    """
    Фильтры для поиска квартир.

    :param flat_id: id квартиры
    :param project_id: id ЖК;
    :param floor: этаж;
    :param rooms: количество комнат;
    :param area: площадь квартиры;
    :param finishing: с отделкой;
    :return: словарь с параметрами поиска.
    """
    result_filter = dict()
    if flat_id:
        result_filter['flat_id'] = flat_id
    if project_id:
        result_filter['project_id'] = project_id
    if floor:
        result_filter['floor'] = floor
    if rooms:
        result_filter['rooms'] = rooms
    if area:
        result_filter['area'] = area
    if finishing == "True":
        result_filter['finishing'] = True
    elif finishing == "False":
        result_filter['finishing'] = False
    return result_filter


def price_filters(
        price_id: int | None = None,
        flat_id: int | None = None,
        benefit_name: str | None = None,
        price: int | None = None,
        meter_price: int | None = None,
        booking_status: str | None = None
) -> dict[str: int | str]:
    """
    Фильтры для поиска цен на квартиры.

    :param price_id: id цены на квартиру;
    :param flat_id: id квартиры
    :param benefit_name: названия ценового предложения;
    :param price: цена;
    :param meter_price: цена за метр;
    :param booking_status: статус брони;
    :return: словарь с параметрами поиска.
    """
    result_filter = dict()
    if price_id:
        result_filter['price_id'] = price_id
    if flat_id:
        result_filter['flat_id'] = flat_id
    if benefit_name:
        result_filter['benefit_name'] = benefit_name
    if price:
        result_filter['price'] = price
    if meter_price:
        result_filter['meter_price'] = meter_price
    if booking_status:
        result_filter['booking_status'] = booking_status
    return result_filter
