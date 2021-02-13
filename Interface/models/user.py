from Interface import db
from sqlalchemy.sql import func
from Interface.models import CurrentAPIMixin


class User(CurrentAPIMixin, db.Model):
    __tablename__ = 'm_user'
    # 用户ID
    userID = db.Column(db.Integer, primary_key=True)
    # 用户名
    userName = db.Column(db.String)
    # 用户名
    nickName = db.Column(db.String)
    # 密码
    password = db.Column(db.String)
    # 创建时间
    createTime = db.Column(db.DATETIME, nullable=True, server_default=func.now())
    # 创建人
    creatorID = db.Column(db.Integer, db.ForeignKey('m_user.userID'))
    creator = db.relationship('User', remote_side=[userID])
    # 禁止状态
    deleteStatus = db.Column(db.Boolean, default=0)

    def __repr__(self):
        return '<User {}>'.format(self.userName)

    def to_login_dict(self):
        if not self:
            return None
        return {
            'userID': self.userID,
            'userName': self.userName,
            'nickName': self.nickName,
            'password': self.password,
            'createTime': str(self.createTime),
            'deleteStatus': self.deleteStatus
        }

    def to_dict(self):
        if not self:
            return None
        return {
            'userID': self.userID,
            'userName': self.userName,
            'nickName': self.nickName,
            'createTime': str(self.createTime),
            'deleteStatus': self.deleteStatus
        }
