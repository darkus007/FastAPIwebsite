"""
Модуль содержит фильтры поиска для роутеров.

Если необходимо расширить фильтр, то просто добавляем новый аргумент функции,
название которого соответствует свойству (атрибуту) модели из файла models.py
"""


def project_filters(
        project_id: int | None = None,
        city: str | None = None,
        name: str | None = None,
        metro: str | None = None
):
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
