

from flask import g

from api.models.message import Message
from api.modules.message import msg_blu
from api.utils.common import auth_identify
from api.utils.response_utils import success


@msg_blu.route("/new", methods=['GET'])
@auth_identify
def new():
    """
    获取用户未读的消息,查找最新的消息
    :return:
    """
    user = g.user
    user_id = user.id
    last_message_read_time = user.last_message_read_time
    msgs = Message.query.filter_by(recipient_id=user_id).filter(
        Message.timestamp > last_message_read_time
    ).all()
    return success(msg='获取用户未读消息成功', data=[i.to_dict() for i in msgs])


@msg_blu.route("/new_count", methods=['GET'])
@auth_identify
def new_count():
    return success(msg='获取用户新消息数成功', data=g.user.new_messages_counts())
