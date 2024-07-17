from app import create_app
import threading

app = create_app()

if __name__ == '__main__':
    app.run(port=5000, threaded=True)