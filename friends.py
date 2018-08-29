# # coding=utf-8

# from sqlalchemy import Column, String, Integer, Date, Text, Boolean, Tinyint

# from base import Base


# class Friends(Base):
#     __tablename__ = 'friends'

#     relations_id = Column(Integer, primary_key=True)
#     first_user = Column(Integer, nullable=False)
#     second_user = Column(Integer, nullable=False)
#     status = Column(Tinyint, nullable=False)

#     def __init__(self, user_id):
#         self.user_id = user_id
