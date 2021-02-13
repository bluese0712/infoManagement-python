from Interface import db
from Interface.models import CurrentAPIMixin


class Fund(CurrentAPIMixin, db.Model):
    __tablename__ = 'cw_m_fund'
    # 基金ID
    fundID = db.Column(db.Integer, primary_key=True)
    # 基金编码
    fundCode = db.Column(db.String)
    # 基金名称
    fundName = db.Column(db.String)
    # 基金类型
    fundType = db.Column(db.String)
    # 基金名称拼音
    fundNamePinyin = db.Column(db.String)
    # 基金拼音缩写
    fundNameAbbreviatedPinyin = db.Column(db.String)
    # 是否删除
    deleteStatus = db.Column(db.Boolean)

    def __repr__(self):
        return '<Fund {}>'.format(self.fundName)

    def to_dict(self):
        return {
            'fundID': self.fundID,
            'fundCode': self.fundCode,
            'fundName': self.fundName,
            'fundType': self.fundType,
            'fundNamePinyin': self.fundNamePinyin,
            'fundNameAbbreviatedPinyin': self.fundNameAbbreviatedPinyin,
            'deleteStatus': self.deleteStatus
        }

    def to_filter_dict(self):
        return {
            'fundID': self.fundID,
            'fundCode': self.fundCode,
            'fundName': self.fundName
        }


def batch_add_info(fund_array):
    try:
        db.session.execute(
            Fund.__table__.insert(),
            [
                {
                    "fundCode": item[0],
                    "fundNameAbbreviatedPinyin": item[1],
                    "fundName": item[2],
                    "fundType": item[3],
                    "fundNamePinyin": item[4]
                }
                for item in fund_array
            ]
        )
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(e)
        return False
    return True
