

from flask import Blueprint

from . import profile, rtmp, channel


def create_bp():
    live_blu = Blueprint('live', __name__, url_prefix='/live')
    profile.api.register(live_blu, url_prefix='/users')
    rtmp.api.register(live_blu, url_prefix='/rtmp')
    channel.api.register(live_blu, url_prefix='/channel')
    return live_blu


live_blu = create_bp()
