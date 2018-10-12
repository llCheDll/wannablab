def row2dict(row):
    return dict([(col.name, str(getattr(row, col.name))) for col in row.__table__.columns])

# def row2dict_limited(row, fields):
#     limited_dict = {}
#
#     for field in fields:
#         limited_dict.update({field: getattr(row, field)})
#
#     return limited_dict
