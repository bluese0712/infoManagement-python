from Interface import db
from Interface.models import CurrentAPIMixin
from datetime import datetime


class FundInfo(CurrentAPIMixin, db.Model):
    __tablename__ = 'cw_t_fund_info'
    # 更新时间
    updateTime = db.Column(db.DATETIME, primary_key=True, default=datetime.now)
    # 更新内容
    updateInfo = db.Column(db.String)

    def __repr__(self):
        return '<FundInfo {}>'.format(self.updateTime)

    def to_dict(self):
        return {
            'updateTime': str(self.updateTime),
            'updateInfo': self.updateInfo
        }
