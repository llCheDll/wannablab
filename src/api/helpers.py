def row2dict(row):
    return dict([(col.name, str(getattr(row, col.name))) for col in row.__table__.columns])
