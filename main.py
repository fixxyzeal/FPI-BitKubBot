from flask import Flask, jsonify, request
from flask_httpauth import HTTPBasicAuth
import bl
app = Flask(__name__)
auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(username, password):
    res = bl.Authenticate(username, password)
    if not res:
        return False
    return True


@app.route("/")
def Index() -> str:
    return jsonify({"message": "FPI BitKubBot"})


@app.route("/trading", methods=['POST'])
@auth.login_required
def Trading() -> str:
    # Call Trading BL Logic
    name = request.json['Name']
    for n in name:
        bl.Trading(n)
    return jsonify({"message": "OK"})


if __name__ == '__main__':
    app.run(debug=False)
