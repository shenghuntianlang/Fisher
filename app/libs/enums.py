"""
the Enum for drift exchanges pending
"""
from enum import Enum


class PendingStatus(Enum):
    """
    交易状态
    """
    # 等待
    Waiting = 1
    # 成功
    Success = 2
    # 拒绝
    Reject = 3
    # 撤销
    Redraw = 4

    @classmethod
    def pending_str(cls, status, identity):
        """
        根据鱼漂状态和用户身份返回对应字符串
        :param status:
        :param identity:
        :return:
        """
        key_map = {
            # 在枚举类内部使用枚举变量时,可以将枚举变量当做类变量
            cls.Waiting: {
                'requester': '等待对方邮寄',
                'gifter': '等待你邮寄'
            },
            cls.Success: {
                'requester': '对方已邮寄',
                'gifter': '你已邮寄,交易完成'
            },
            cls.Reject: {
                'requester': '对方已拒绝',
                'gifter': '你已拒绝'
            },
            cls.Redraw: {
                'requester': '你已撤销',
                'gifter': '对方已撤销'
            }
        }
        return key_map[status][identity]
