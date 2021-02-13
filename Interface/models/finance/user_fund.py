from Interface import db
from Interface.models import CurrentAPIMixin, Fund


class CWUserFund(CurrentAPIMixin, db.Model):
    __tablename__ = 'cw_t_user_fund'
    # 用户基金记录ID
    userFundID = db.Column(db.Integer, primary_key=True)
    # 用户ID
    userID = db.Column(db.Integer)
    # 基金ID
    fundID = db.Column(db.Integer, db.ForeignKey('cw_m_fund.fundID'))
    fund = db.relationship('Fund')
    # 购买版本
    version = db.Column(db.Integer)
    # 购买时间
    bitTime = db.Column(db.TIMESTAMP)
    # 购买净值
    bidNAV = db.Column(db.Float)
    # 购买份额
    bidShare = db.Column(db.Float)
    # 最新净值
    latestNAV = db.Column(db.Float)
    # 最新更新时间
    latestTime = db.Column(db.TIMESTAMP)
    # 出售时间
    offerTime = db.Column(db.TIMESTAMP, nullable=True)
    # 出售净值
    offerNAV = db.Column(db.Float, nullable=True)
    # 出售份额
    offerShare = db.Column(db.Float, nullable=True)
    # 赎回费
    redemptionPrice = db.Column(db.Float, nullable=True)
    # 购买类型 0:正常购买 1:分红购买
    type = db.Column(db.Boolean, default=0)
    # 删除状态
    deleteStatus = db.Column(db.Boolean, default=0)
    # 当前状态 0:未赎回 1:部分赎回 2:已赎回
    status = db.Column(db.Integer, default=0)

    def __repr__(self):
        return '<Department {}>'.format(self.userFundID)

    def to_dict(self):
        return {
            'userFundID': self.userFundID,
            'userID': self.userID,
            'fundID': self.fundID,
            'fund': None if not self.fund else Fund.to_dict(self.fund),
            'version': self.version,
            'bitTime': str(self.bitTime),
            'bidNAV': self.bidNAV,
            'bidShare': self.bidShare,
            'latestNAV': self.latestNAV,
            'latestTime': str(self.latestTime),
            'offerTime': None if not self.offerTime else str(self.offerTime),
            'offerNAV': self.offerNAV,
            'offerShare': self.offerShare,
            'redemptionPrice': self.redemptionPrice,
            'type': self.type,
            'deleteStatus': self.deleteStatus,
            'status': self.status
        }
