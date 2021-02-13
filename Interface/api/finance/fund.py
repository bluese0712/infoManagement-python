import json
import re
import datetime
import requests
from flask import request, session
from Interface.api import cw_fund_api
from Interface.utils import is_login, Success, Fail, return_json, form_has_parameter as validate, date_string_to_date
from Interface.models import Fund, batch_add_info, FundInfo, CWRedemptionRule, CWUserFund, batch_add_rule
from sqlalchemy import or_, and_


# 获取用户所有基金
@cw_fund_api.route('/getUserFundList', methods=['POST'])
@is_login
def get_user_fund_list():
    user_fund_list = CWUserFund.query.filter(CWUserFund.deleteStatus == 0).all()
    array = []
    for item in user_fund_list:
        array.append(CWUserFund.to_dict(item))
    return return_json(Success(data=array))


# 根据条件获取基金记录列表(添加时模拟匹配用)
@cw_fund_api.route('/getFundListByParams', methods=['POST'])
@is_login
def get_fund_list_by_params():
    if not request.form.get('matchField'):
        return return_json(Success(data=[]))
    match_str = '%' + request.form.get('matchField') + '%'
    task_filter = {
        and_(
            Fund.deleteStatus == 0,
            or_(
                Fund.fundCode.like(match_str),
                Fund.fundName.like(match_str),
                Fund.fundNamePinyin.like(match_str),
                Fund.fundNameAbbreviatedPinyin.like(match_str)
            )
        )
    }
    fund_list = Fund.query.filter(*task_filter).limit(100).all()
    array = []
    for item in fund_list:
        array.append(Fund.to_filter_dict(item))
    return return_json(Success(data=array))


# 获取指定日期净值
@cw_fund_api.route('/getFundEquityByFundCode', methods=['POST'])
@is_login
def get_fund_equity_by_fund_code():
    required = validate(request.form, [{'fundID': '基金为空'}, {'confirmationTime': '确购日期为空'}])
    if required:
        return return_json(Fail(msg=required))
    date = date_string_to_date(request.form.get('confirmationTime'), '%Y-%m-%d %H:%M:%S')
    if not date:
        return return_json(Fail(msg='确购日期错误'))
    fund = Fund.query.get(request.form.get('fundID'))
    if not fund:
        return return_json(Fail(msg='基金错误'))
    end_date = date + datetime.timedelta(days=-1)
    record = get_latest_net_value_of_hybrid_fund(fund.fundCode, None, end_date, 1)[0]
    return return_json(Success(data=record))


# 添加角色所有基金和赎回规则
@cw_fund_api.route('/addUserFundAndRedemptionRules', methods=['POST'])
@is_login
def add_user_fund_and_redemption_rules():
    required = validate(request.form, [{'fundID': '基金ID为空'}, {'bitTime': '确购日期为空'},
                                       {'bidNAV': '确购净值为空'}, {'bidShare': '确购份额为空'}])
    if required:
        return return_json(Fail(msg=required))
    # 判断基金是否存在
    fund = Fund.query.get(request.form.get('fundID'))
    if not fund:
        return return_json(Fail(msg='基金错误'))
    last_user_fund = CWUserFund.query.\
        filter(CWUserFund.userID == session.get(request.cookies.get("BLUE_FEATHER_SESSION")).get('userID')).\
        filter(CWUserFund.fundID == fund.fundID).order_by(CWUserFund.version.desc()).first()

    record = get_latest_net_value_of_hybrid_fund(fund.fundCode, None, None, 1)[0]

    user_fund = CWUserFund(userID=session.get(request.cookies.get("BLUE_FEATHER_SESSION")).get('userID'),
                           fundID=request.form.get('fundID'),
                           version=1 if not last_user_fund else last_user_fund.version + 1,
                           bitTime=date_string_to_date(request.form.get('bitTime'), '%Y-%m-%d %H:%M:%S'),
                           bidNAV=request.form.get('bidNAV'),
                           bidShare=request.form.get('bidShare'),
                           latestNAV=float(record.get('DWJZ')),
                           latestTime=datetime.datetime.now())

    rule_array = []
    if request.form.get('rules'):
        rules = json.loads(request.form.get('rules'))
        for rule in rules:
            rule_array.append([session.get(request.cookies.get("BLUE_FEATHER_SESSION")).get('userID'),
                               fund.fundID, 1 if not last_user_fund else last_user_fund.version + 1,
                               rule.get('minDays'),
                               None if not rule.get('maxDays') else rule.get('maxDays'), rule.get('rate')])

    if not user_fund.to_add(user_fund):
        return return_json(Fail(msg='用户基金创建错误'))

    if len(rule_array) != 0 and not batch_add_rule(rule_array):
        user_fund.to_delete(user_fund)
        return return_json(Fail(msg='用户基金赎回规则创建错误'))
    return return_json(Success(data='创建成功'))


# 追加购买基金
@cw_fund_api.route('/appendUserFund', methods=['POST'])
@is_login
def append_user_fund():
    required = validate(request.form, [{'userFundID': '基金ID为空'}, {'bitTime': '确购日期为空'},
                                       {'bidNAV': '确购净值为空'}, {'bidShare': '确购份额为空'}])
    if required:
        return return_json(Fail(msg=required))
    # 判断基金是否存在
    user_fund = CWUserFund.query.get(request.form.get('userFundID'))
    if not user_fund:
        return return_json(Fail(msg='拥有基金记录错误'))

    user_fund = CWUserFund(userID=session.get(request.cookies.get("BLUE_FEATHER_SESSION")).get('userID'),
                           fundID=user_fund.fundID,
                           version=user_fund.version,
                           bitTime=date_string_to_date(request.form.get('bitTime'), '%Y-%m-%d %H:%M:%S'),
                           bidNAV=request.form.get('bidNAV'),
                           bidShare=request.form.get('bidShare'),
                           latestNAV=user_fund.latestNAV,
                           latestTime=user_fund.latestTime)
    return return_json(Success(data='创建成功')) if user_fund.to_add(user_fund) else return_json(Fail(msg='追加购买错误'))


# 获取基金数据
def get_latest_net_value_of_hybrid_fund(fund_code, start_time: datetime, end_time: datetime, page_size=1):
    url = 'http://api.fund.eastmoney.com/f10/lsjz'

    # 参数化访问链接，以dict方式存储
    params = {
        'callback': 'jQuery18302183990854851532_1610004838519',
        'fundCode': fund_code,
        'pageIndex': 1,
        'pageSize': page_size,
    }
    if start_time:
        params['startDate'] = start_time.strftime("%Y-%m-%d")
    if end_time:
        params['endDate'] = end_time.strftime("%Y-%m-%d")
    # 装饰头文件
    headers = {
        'Host': 'api.fund.eastmoney.com',
        'Referer': 'http://fundf10.eastmoney.com/jjjz_%s.html' % fund_code,
    }
    res = requests.get(url=url, headers=headers, params=params)  # 发送请求
    content = re.findall('jQuery18302183990854851532_1610004838519[(](.*})', res.text)[0]
    data = json.loads(content)
    return data['Data']['LSJZList']


# 更新基金并做更新记录
def update_fund():
    last_fund_info = FundInfo.query.order_by(FundInfo.updateTime.desc()).first()
    interval = datetime.datetime.now() - last_fund_info.updateTime
    if interval.day < 6:
        return True
    last_fund = Fund.query.order_by(Fund.fundID.desc()).first()
    res = requests.get('http://fund.eastmoney.com/js/fundcode_search.js')
    content = re.findall('var r = (.*])', res.text)[0]
    fund_array = json.loads(content)
    add_array = []
    if not last_fund:
        add_array = fund_array.copy()
    else:
        is_search = False
        for fund in fund_array:
            if is_search:
                add_array.append(fund)
                continue
            if fund[0] == last_fund.fundCode:
                is_search = True
    need_add_info = False
    if len(add_array) != 0:
        need_add_info = batch_add_info(add_array)
    else:
        need_add_info = True
    if need_add_info:
        FundInfo.to_add(FundInfo(updateInfo='本次更新' + str(len(add_array)) + '个基金'))
