
from datetime import datetime

from api import db
from api.libs.db_utils import session_commit


class BaseModels:
    """模型基类"""
    create_time = db.Column(db.DateTime, default=datetime.now)  # 创建时间
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)  # 记录你的更新时间
    status = db.Column(db.SmallInteger, default=1)  # 记录存活状态

    def add(self, obj):
        db.session.add(obj)
        return session_commit()

    def update(self):
        return session_commit()

    def delete(self):
        self.status = 0
        return session_commit()
