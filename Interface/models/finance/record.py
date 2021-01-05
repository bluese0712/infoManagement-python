from sqlalchemy import func
from Interface import db
from Interface.models import CurrentAPIMixin, CWCategory


# 部门
class CWRecord(CurrentAPIMixin, db.Model):
    __tablename__ = 'cw_t_record'
    # 记录ID
    recordID = db.Column(db.Integer, primary_key=True)
    # 所属类别
    categoryID = db.Column(db.Integer, db.ForeignKey('cw_m_category.categoryID'))
    category = db.relationship('CWCategory')
    # 用户ID
    userID = db.Column(db.Integer)
    # 金额
    amount = db.Column(db.Numeric)
    # 消费时间
    dissipate = db.Column(db.DATETIME, server_default=func.now())
    # 创建时间
    createTime = db.Column(db.DATETIME, server_default=func.now())
    # 禁用状态
    deleteStatus = db.Column(db.Boolean, default=0)

    def __repr__(self):
        return '<Department {}>'.format(self.recordID)

    def to_dict(self):
        return {
            'recordID': self.recordID,
            'categoryID': self.categoryID,
            'category': CWCategory.to_dict(self.category),
            'userID': self.userID,
            'amount': float(self.amount),
            'dissipate': str(self.dissipate),
            'createTime': str(self.createTime),
            'deleteStatus': self.deleteStatus
        }


# 更新用户
def update_department(department: CWRecord, department_name):
    try:
        department.departmentName = department_name
        db.session.commit()
    except():
        return False
    return True


# 批量添加部门
def batch_add_department(recipient_list, create_id):
    try:
        db.session.execute(
            CWRecord.__table__.insert(),
            [{"departmentName": item, "creatorID": create_id} for item in recipient_list]
        )
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(e)
        return False
    return True
