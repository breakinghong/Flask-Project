

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from api.models.user import UserInfo
from api.models.video import VideoInfo
from api.models.content import ContentMain
from api.models.gitinfo import GithubInfo
from flask_cors import CORS
from api import db, create_app

app = create_app('dev')

CORS(app, supports_credentials=True)

manager = Manager(app)
Migrate(app, db)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
