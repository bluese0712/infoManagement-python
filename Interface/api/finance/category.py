from Interface.api import cw_category_api
from flask import request, session
from Interface.utils import is_login, Success, Fail, return_json, form_has_parameter as validate
from Interface.models import CWCategory


# 创建收支项
@cw_category_api.route('/createCategory', methods=['POST'])
@is_login
def create_category():
    required = validate(request.form, [{'categoryName': '项目名为空'}])
    if required:
        return return_json(Fail(msg=required))
    parent = None
    if request.form.get('categoryID'):
        parent = CWCategory.query.get(request.form.get('categoryID'))
        if not parent:
            return return_json(Fail(msg='主项ID错误'))
    elif not request.form.get('type'):
        return return_json(Fail(msg='收支项类型为空'))
    else:
        c_type = int(request.form.get('type'))
        if c_type != 0 and c_type != 1 and c_type != 2:
            return return_json(Fail(msg='收支项类型错误'))
    category = CWCategory(categoryName=request.form.get('categoryName'),
                          parentID=0 if not parent else parent.categoryID,
                          type=request.form.get('type') if not parent else parent.type)
    return return_json(Success(msg='添加成功') if CWCategory.to_add(category) else Fail(msg='添加失败'))


# 编辑收支项
@cw_category_api.route('/editCategory', methods=['POST'])
@is_login
def edit_category():
    required = validate(request.form, [{'categoryID': '项目ID为空'}, {'categoryName': '项目名为空'}])
    if required:
        return return_json(Fail(msg=required))
    category = CWCategory.query.get(request.form.get('categoryID'))
    if not category:
        return return_json(Fail(msg='项目ID错误'))
    category.categoryName = request.form.get('categoryName')
    return return_json(Success(msg='编辑成功') if category.to_update() else Fail(msg='编辑失败'))


# 删除收支项
@cw_category_api.route('/deleteCategory', methods=['POST'])
@is_login
def delete_category():
    required = validate(request.form, [{'categoryID': '项目ID为空'}])
    if required:
        return return_json(Fail(msg=required))
    category = CWCategory.query.get(request.form.get('categoryID'))
    if not category:
        return return_json(Fail(msg='项目ID错误'))
    children_category = CWCategory.query.filter(CWCategory.parentID == request.form.get('categoryID')).all()
    children_category.append(category)
    return return_json(Success(msg='删除成功') if CWCategory.to_delete_list(children_category) else Fail(msg='删除失败'))


# 获取所有子项
@cw_category_api.route('/getChildrenCategory', methods=['POST'])
@is_login
def get_children_category():
    required = validate(request.form, [{'type': '收支项目类型为空'}])
    if required:
        return return_json(Fail(msg=required))
    record = CWCategory.query.filter(CWCategory.type == 1).filter(CWCategory.parentID != 0).all()
    category_list = []
    for category in record:
        category_list.append(CWCategory.to_dict(category))
    return return_json(Success(data=category_list))


# 获取所有收支项
@cw_category_api.route('/getAllCategory', methods=['GET'])
@is_login
def get_all_category():
    record = CWCategory.query.filter(CWCategory.deleteStatus == 0).all()
    category_list = []
    for category in record:
        category_list.append(CWCategory.to_dict(category))
    return return_json(Success(data=category_list))
