from flask import Blueprint, request, abort, jsonify, current_app, g
from jsonschema import validate, ValidationError
from os import path, unlink
from docker.errors import ContainerError, NotFound
from ..hooks import auth
from ..schemas.create import create_schema
import json

app = Blueprint('toxbot', __name__)

@app.route('/create', methods=["POST"])
@auth.login_required
def create():
    if request.json:
        body = request.json
        try:
            validate(body, create_schema)
            logs_path = path.normpath(path.join(path.dirname(__file__), '../../../logs'))
            current_app.logger.debug("logs path %s" % logs_path)

            c = g.docker.run(env={
                "TIMEOUT" : 1,
                "BOTNAME" : body.get("name"),
                "DTH_HOST_CONNECTION_TIMEOUT": 100,
                "DEBUG": body.get("debug") if body.get("debug") is not None else 0,
                "PROXY_TYPE": body.get("proxy_type") if body.get("proxy_type") is not None else 0,
                "PROXY_HOST": body.get("proxy_host") if body.get("proxy_host") is not None else "localhost",
                "PROXY_PORT": body.get("proxy_port") if body.get("proxy_port") is not None else 9150,
                "DHT_NODE_LIST_URL": "https://nodes.tox.chat/json",
                "API_ADMIN_ENDPOINT": body.get("api_admin_endpoint"),
                "WELCOME_MESSAGE": body.get("welcome_message") if body.get("welcome_message") is not None else 'Hi!',
                "USE_SSL": body.get("use_ssl") if body.get("use_ssl") is not None else 0
            }, volumes={
                logs_path : {'bind': '/opt/toxbot/logs', 'mode': 'rw'}
            })

            current_app.logger.debug("Save id [%s][%s]" % (current_app.config['IDS_PATH'], c.short_id))
            id_file_path = "%s/%s" % (current_app.config['IDS_PATH'], c.short_id)

            with open(id_file_path, 'at') as f:
                f.write(c.short_id)

            return jsonify(status="success", id=c.short_id, name=body.get("name"))
        except ValidationError as err:
            return jsonify(error_message="Create tox bot error", error = str(err)), 400
        except ContainerError as err:
            return jsonify(error_message="Create tox bot container error", error = str(err)), 400

@app.route('/logs/<bot_id>', methods=["GET"])
@auth.login_required
def logs(bot_id):
    try:
        c = g.docker.getC(bot_id)
        logs = c.logs()
        current_app.logger.debug(logs)
        return jsonify(status="success")
    except NotFound as err:
        return jsonify(error_message="Bot container not found", error = str(err)), 404

@app.route('/status/<bot_id>', methods=["GET"])
@auth.login_required
def status(bot_id):
    try:
        c = g.docker.getC(bot_id)
        stats = c.stats(decode=True, stream=False)
        return jsonify(status="success", stats=stats)
    except NotFound as err:
        return jsonify(error_message="Bot container not found", error = str(err)), 404

@app.route('/delete/<bot_id>', methods=["DELETE"])
@auth.login_required
def delete(bot_id):
    try:
        c = g.docker.getC(bot_id)
        c.remove(force=True)
        id_file_path = "%s/%s" % (current_app.config['IDS_PATH'], c.short_id)
        unlink(id_file_path)
        return jsonify(status="success", id=c.short_id)
    except NotFound as err:
        return jsonify(error_message="Bot container not found", error = str(err)), 404
