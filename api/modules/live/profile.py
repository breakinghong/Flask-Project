

from flask import jsonify
from api.libs.redprint import Redprint

api = Redprint('profile')



@api.route('/profile')
def profile():

    data = {
        'time_data': 1,
        'count_data': 2,
    }
    return jsonify(data)
