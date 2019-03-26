
from gevent import monkey
from  gevent.pywsgi import WSGIServer

monkey.patch_all()



if __name__ == '__main__':
    from app import create_app
    app = create_app()
    from app.celery.main import celery
    http_server = WSGIServer(('127.0.0.1', 5000), app)
    http_server.serve_forever()
    # app.run()

