from flask import Flask, Blueprint
from flask_restplus import Api

from app.config import configuration


def create_app(config):
    '''
    This function creates a flask instance

    Parameters:
      config (dict): Contains env variables.

    Returns:
      a flask instance.

    '''
    app = Flask(__name__, instance_relative_config=True, static_folder=None)
    app.config.from_object(configuration[config])
    app.url_map.strict_slashes = False

    # initialize api
    api = Api(app=app,
              title='Code challenge',
              doc='',
              description='')

    from app.views import api as health

    api.add_namespace(health, path='/api/v1')

    return app
