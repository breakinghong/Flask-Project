

import logging
import os
from dotenv import load_dotenv
from flask import Flask, current_app, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_uploads import UploadSet, IMAGES, configure_uploads, patch_request_class
from redis import StrictRedis
from flask_session import Session
from api.utils.log_utils import setup_log
from config.config import config_dict

db = SQLAlchemy()
redis_store = None
APP_ROOT = os.path.join(os.path.dirname(__file__), "..")
dotenv_path = os.path.join(APP_ROOT, ".env")
load_dotenv(dotenv_path)

# Initialize Flask-Uploads
photos = UploadSet('photos', IMAGES)


def create_app(config_name):
    app = Flask(__name__)
    config = config_dict.get(config_name)
    setup_log(log_file='logs/root.log', level=config.LEVEL_LOG)
    app.config.from_object(config)
    Session(app)
    db.init_app(app)

    configure_uploads(app, photos)
    patch_request_class(app)
    # log
    # gunicorn_logger = logging.getLogger('gunicorn.error')
    # app.logger.handlers = gunicorn_logger.handlers
    # app.logger.setLevel(gunicorn_logger.level)
    # app.logger.info('nihao')
    # @app.before_request
    # def before_request():
    #     interface = request.path
    #     print(interface)
    #     if '/login' in interface:
    #         return None
    #     else:
    #         if request.method == 'OPTIONS':
    #             pass
    #         else:
    #             print('**'*50)
    #             redirect(interface)
    #
    @app.after_request
    def add_header(response):
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Headers'] = '*'
        response.headers['Access-Control-Request-Method'] = "POST, PUT, GET, OPTIONS, DELETE"
        return response

    global redis_store
    # 创建redis的连接对象
    redis_store = StrictRedis(host=config.REDIS_HOST, port=config.REDIS_PORT, decode_responses=True)

    from api.modules.index import index_blu
    app.register_blueprint(index_blu)

    from api.modules.passport import passport_blu
    app.register_blueprint(passport_blu)

    from api.modules.auth import auth_blu
    app.register_blueprint(auth_blu)

    from api.modules.profile import profile_blu
    app.register_blueprint(profile_blu)

    from api.modules.video import video_blu
    app.register_blueprint(video_blu)

    from api.modules.message import msg_blu
    app.register_blueprint(msg_blu)

    from api.modules.admin import create_bp_admin
    app.register_blueprint(create_bp_admin())

    from api.modules.live import live_blu
    app.register_blueprint(live_blu)

    return app
