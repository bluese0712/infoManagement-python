from Interface import db
from Interface.models import CurrentAPIMixin


class CWRedemptionRule(CurrentAPIMixin, db.Model):
    __tablename__ = 'cw_t_redemption_rule'
    # 类别ID
    redemptionRuleID = db.Column(db.Integer, primary_key=True)
    # 用户ID
    userID = db.Column(db.Integer)
    # 基金ID
    fundID = db.Column(db.Integer)
    # 购买版本
    version = db.Column(db.Integer)
    # 小于等于的天数
    minDays = db.Column(db.Integer)
    # 大于的天数
    maxDays = db.Column(db.Integer, nullable=True)
    # 赎回费率
    rate = db.Column(db.Float)

    def __repr__(self):
        return '<Department {}>'.format(self.redemptionRuleID)

    def to_dict(self):
        return {
            'redemptionRuleID': self.redemptionRuleID,
            'userID': self.userID,
            'fundID': self.fundID,
            'version': self.version,
            'minDays': self.minDays,
            'maxDays': self.maxDays,
            'rate': self.rate
        }


def batch_add_rule(rule_array):
    try:
        db.session.execute(
            CWRedemptionRule.__table__.insert(),
            [
                {
                    "userID": item[0],
                    "fundID": item[1],
                    "version": item[2],
                    "minDays": item[3],
                    "maxDays": item[4],
                    "rate": item[5]
                }
                for item in rule_array
            ]
        )
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(e)
        return False
    return True