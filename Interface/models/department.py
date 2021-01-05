# from sqlalchemy import func
# from Interface import db
# from Interface.models import CurrentAPIMixin
#
#
# # 部门
# class Department(CurrentAPIMixin, db.Model):
#     __tablename__ = 'm_department'
#     # # 部门ID
#     # departmentID = db.Column(db.Integer, primary_key=True)
#     # # 部门名字
#     # departmentName = db.Column(db.String)
#     # # 父节点ID
#     # parentID = db.Column(db.Integer, db.ForeignKey('m_department.departmentID'), nullable=True)
#     # parent = db.relationship(
#     #     'Department',
#     #     remote_side=[departmentID],
#     #     backref=db.backref('child', lazy='dynamic'),
#     # )
#     # # 发送优先级
#     # sendingPriority = db.Column(db.Integer, default=3)
#     # # 创建者ID
#     # creatorID = db.Column(db.Integer, db.ForeignKey('m_user.userID'))
#     # creator = db.relationship('User')
#     # # 创建时间
#     # createTime = db.Column(db.DATETIME, server_default=func.now())
#     # # 禁用状态
#     # forbidStatus = db.Column(db.Boolean, default=0)
#     # users = db.relationship('Recipient', backref='department', lazy="dynamic")
#
#     def __repr__(self):
#         return '<Department {}>'.format(self.departmentName)
#
#     def to_dict(self):
#         return {
#             'departmentID': self.departmentID,
#             'departmentName': self.departmentName,
#             'parentID': self.parentID,
#             'parent': None if not self.parent else Department.to_dict(self.parent),
#             'sendingPriority': self.sendingPriority,
#             'creator': User.to_dict(self.creator),
#             'createTime': str(self.createTime),
#             'forbidStatus': self.forbidStatus
#         }
#
#     def to_tree(self):
#         return {
#             'departmentID': self.departmentID,
#             'departmentName': self.departmentName,
#             'parentID': self.parentID,
#             'sendingPriority': self.sendingPriority,
#             # 'creator': User.to_dict(self.creator),
#             'createTime': str(self.createTime),
#             'forbidStatus': self.forbidStatus,
#             'users': [item.to_tree() for item in self.users]
#         }
#
#
# # 更新用户
# def update_department(department: Department, department_name):
#     try:
#         department.departmentName = department_name
#         db.session.commit()
#     except():
#         return False
#     return True
#
#
# # 批量添加部门
# def batch_add_department(recipient_list, create_id):
#     try:
#         db.session.execute(
#             Department.__table__.insert(),
#             [{"departmentName": item, "creatorID": create_id} for item in recipient_list]
#         )
#         db.session.commit()
#     except Exception as e:
#         db.session.rollback()
#         print(e)
#         return False
#     return True
