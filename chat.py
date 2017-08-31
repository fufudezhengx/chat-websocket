#!/bin/env python
from flask import Flask
from routes import main as main_blueprint
from events import socketio


def configured_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'gua'

    app.register_blueprint(main_blueprint)

    socketio.init_app(app)
    return app


if __name__ == '__main__':
    app = configured_app()
    app.debug = True
    socketio.run(app, host='0.0.0.0', port=80)
