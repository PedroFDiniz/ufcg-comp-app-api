from application import app
from application.utils.constants import PORT, HOST

if __name__ == '__main__':
    app.run(host=HOST, port=PORT, debug=True)
    # server = Server(app.wsgi_app)
    # server.serve(host=HOST, port=PORT, debug=True)
    
