from db import models


def row2dict(row):
    return dict([(col.name, str(getattr(row, col.name))) for col in row.__table__.columns])


def query2list(items_list, depth=0):
    """
    Convert sqlalchemy request from database to list of dictionaries. Nested objects
     within the specified 'depth' are converted the same.
    :param items_list: query from sqlalchemy database to be transferred to list of dictionaries
    :param depth: max level of nested objects to be disclosure.
     The last level is disclosed as name of class.
    :return: list of dictionaries
    """
    data_list = []

    for item in items_list:
        item_dict = {}

        for key in item.__mapper__._props.keys():
            if depth > 0 and isinstance(getattr(item, key), list):
                item_dict[key] = query2list(getattr(item, key), depth - 1)
            elif (depth > 0 and
                  getattr(getattr(item, key), '__module__', None) == models.__name__
            ):
                item_dict[key] = query2list([getattr(item, key)], depth - 1)

            else:
                item_dict[key] = str(getattr(item, key))

        data_list.append(item_dict)

    return data_list
