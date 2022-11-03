from application import app, PORT, HOST
from livereload import Server


if __name__ == '__main__':
    app.run(host=HOST, port=PORT, debug=True)
    # server = Server(app.wsgi_app)
    # server.serve(host=HOST, port=PORT, debug=True)
    
