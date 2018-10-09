from flask import g
from flask_httpauth import HTTPTokenAuth

auth = HTTPTokenAuth(scheme='Token')

tokens = {
    "secret_key": "john",
    "secret_key2": "susan"
}

@auth.verify_token
def verify_token(token):
    if token in tokens:
        g.current_user = tokens[token]
        return True
    return False