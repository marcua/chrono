from flask import Flask
app = Flask(__name__)

@app.route('/')
def __init__():
    return 'Hello World!'

if __name__ == '__main__':
    app.run()