# -*- coding:utf-8 -*-
__author__ = 'kerry'

from server.app import create_app
app = create_app('local')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
