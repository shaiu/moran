import logging.config
import os
import requests
from flask import Flask

dir_path = os.path.dirname(os.path.realpath(__file__))

API_KEY = os.getenv('API_KEY')


def create_app(test_config=None):
    logging.config.fileConfig(os.path.join(dir_path, 'conf', 'logging.ini'))

    _logger = logging.getLogger(__name__)
    _logger.setLevel(logging.DEBUG)

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/data', methods=['GET'])
    def fetch():
        data = requests.get(
            f'http://moran.mot.gov.il:110/Channels/HTTPChannel/SmQuery/2.8/json?Key={API_KEY}&MonitoringRef=32902')
        return {"data": data.json()}

    return app
