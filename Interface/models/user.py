# from app import db
# from sqlalchemy.sql import func
# from app.models import CurrentAPIMixin
#
#
# class User(CurrentAPIMixin, db.Model):
#     __tablename__ = 'm_user'
#     # 用户ID
#     userID = db.Column(db.Integer, primary_key=True)
#     # 用户名
#     username = db.Column(db.String)
#     # 密码
#     password = db.Column(db.String)
#     # 创建时间
#     createTime = db.Column(db.DATETIME, nullable=True, server_default=func.now())
#     # 禁止状态
#     forbidStatus = db.Column(db.Boolean, default=0)
#
#     def __repr__(self):
#         return '<User {}>'.format(self.username)
#
#     def to_login_dict(self):
#         if not self:
#             return None
#         return {
#             'userID': self.userID,
#             'username': self.username,
#             'password': self.password,
#             'createTime': str(self.createTime),
#             'forbidStatus': self.forbidStatus
#         }
#
#     def to_dict(self):
#         if not self:
#             return None
#         return {
#             'userID': self.userID,
#             'username': self.username,
#             'createTime': str(self.createTime),
#             'forbidStatus': self.forbidStatus
#         }
#
#
# # 更新用户
# def class_update_user(user: User, password):
#     try:
#         user.password = password
#         db.session.commit()
#     except():
#         return False
#     return True
