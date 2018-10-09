from flask import Flask, g, request
from flask_cors import CORS
from os import path
from dotenv import load_dotenv

from . import controllers
from .services.docker import Docker

dotenv_path = path.normpath(path.join(path.dirname(__file__), '../../.env'))
load_dotenv(dotenv_path=dotenv_path)


def init_docker():
    print("Env:", dotenv_path)
    docker_instance = Docker("toxbot_1")
    if not docker_instance.is_image_exist():
        print("Image %s exist" % docker_instance.image_name)
    docker_instance.build()
    return docker_instance


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY='dev',
        IDS_PATH=path.normpath(path.join(path.dirname(__file__), './ids'))
    )
    CORS(app)
    app.register_blueprint(controllers.toxbot.app, url_prefix='/v1/api/toxbot')
    docker = init_docker()
    # with app.app_context():
    #     g.docker = init_docker()
    @app.before_request
    def before_request():
        g.docker = docker
    return app