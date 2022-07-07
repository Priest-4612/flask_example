from flask import Flask

from db.db import init_db

app = Flask(__name__)


@app.route('/hello-world')
def hello_world():
    return 'Hello, World!'


def main():
    init_db()
    app.run(debug=True)


if __name__ == '__main__':
    main()
