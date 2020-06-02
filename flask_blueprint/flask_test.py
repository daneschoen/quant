from flask import Flask

app = Flask(__name__)


PORT = 80  # 5000


@app.route("/")
def hello():
    return "<h1 style='color:blue'>hey - works for mulitple flask running!</h1>"

@app.route("/boo")
def scared():
    return "<h1 style='color:red'>Boo!</h1>"


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=PORT)

"""
Just sanity check wo nginx wired or uwsgi:

# sudo ufw allow 5000

$ python flask_test.py
  python -m flask run flask_test.py
  FLASK_APP=flask_test.py flask run

http://server_domain_or_IP        # nginx welcome
http://server_domain_or_IP:5000   # flask hello there

"""
