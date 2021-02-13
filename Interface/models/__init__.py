from Interface.models.base import CurrentAPIMixin
# 用户
from .user import User
from .finance.category import CWCategory
from .finance.record import CWRecord

# 基金
from .finance.fund import Fund, batch_add_info
# 所有基金信息
from .finance.fun_info import FundInfo
# 用户所拥有的基金
from .finance.user_fund import CWUserFund
# 用户基金的赎回规则
from .finance.redemption_rule import CWRedemptionRule, batch_add_rule
