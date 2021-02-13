from Interface import db


class CurrentAPIMixin(object):
    @staticmethod
    def to_paginate_dict(query, page_number, page_size):
        resources = query.paginate(page_number, page_size, False)
        data = {
            'data': [item.to_dict() for item in resources.items],
            'total': resources.total
        }
        return data

    # 更新数据
    @staticmethod
    def to_update():
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(e)
            return False
        return True

    # 伪删除
    @staticmethod
    def to_delete(model_data):
        try:
            model_data.deleteStatus = 1
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(e)
            return False
        return True

    # 通用添加
    @staticmethod
    def to_add(model_data):
        try:
            db.session.add(model_data)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(e)
            return False
        return True

    # 真删除
    @staticmethod
    def to_delete_physically(model_data):
        try:
            db.session.delete(model_data)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(e)
            return False
        return True

    # 批量删除
    @staticmethod
    def to_delete_list(model_data):
        try:
            for item in model_data:
                item.deleteStatus = 1
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(e)
            return False
        return True

    # 执行sql语句
    @staticmethod
    def to_execute_sql(sql):
        try:
            data = db.session.execute(sql)
            return data
        except Exception as e:
            db.session.rollback()
            print(e)
            return False
