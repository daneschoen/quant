
#from .init_project import *
from apps import app

if __name__ == "__main__":
    #app.static_url_path = "/"
    app.run()

"""
app = Flask(__name__, static_url_path='')

@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('js', path)
"""
