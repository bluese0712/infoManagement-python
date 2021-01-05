from Interface import db
from Interface.models import CurrentAPIMixin


class CWCategory(CurrentAPIMixin, db.Model):
    __tablename__ = 'cw_m_category'
    # 类别ID
    categoryID = db.Column(db.Integer, primary_key=True)
    # 类别名
    categoryName = db.Column(db.String(50))
    # 所属类别
    parentID = db.Column(db.Integer, db.ForeignKey('cw_m_category.categoryID'))
    parent = db.relationship('CWCategory', remote_side=[categoryID])
    # 类型 0为支出 1为收入 2为具体项
    type = db.Column(db.Integer)
    # 是否删除
    deleteStatus = db.Column(db.Boolean)

    def __repr__(self):
        return '<Department {}>'.format(self.categoryName)

    def to_dict(self):
        return {
            'categoryID': self.categoryID,
            'categoryName': self.categoryName,
            'parentID': self.parentID,
            'parent': None if not self.parent else CWCategory.to_dict(self.parent),
            'type': self.type,
            'deleteStatus': self.deleteStatus
        }
