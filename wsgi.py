# -*- coding: utf-8 -*-

from gevent import monkey
monkey.patch_all()

import os

import leancloud

from app import app
from cloud import engine

APP_ID = os.environ['1IlcnkuFFB6rHZ4KYy5MbKWV-gzGzoHsz']
APP_KEY = os.environ['hlDsz3kYtf4RNJ4p9WVuP3BL']
MASTER_KEY = os.environ['i3NgjV7jh3tFofAFqqmqDAI4']
PORT = int(os.environ['3000'])

leancloud.init(APP_ID, app_key=APP_KEY, master_key=MASTER_KEY)
# Set this to be True if you need to access LeanCloud services with Master Key.
leancloud.use_master_key(True)

# Uncomment the following line to redirect HTTP requests to HTTPS.
# app = leancloud.HttpsRedirectMiddleware(app)
app = engine.wrap(app)
application = app

if __name__ == '__main__':
    from gevent.pywsgi import WSGIServer
    from geventwebsocket.handler import WebSocketHandler

    env = os.environ['production']
    if env == 'production':
        server = WSGIServer(('0.0.0.0', PORT), application, log=None, handler_class=WebSocketHandler)
        server.serve_forever()
    else:
        from werkzeug.serving import run_with_reloader
        from werkzeug.debug import DebuggedApplication

        app.debug = True
        application = DebuggedApplication(application, evalex=True)
        address = 'localhost' if env == 'development' else '0.0.0.0'
        server = WSGIServer((address, PORT), application, handler_class=WebSocketHandler)
        run_with_reloader(server.serve_forever)
