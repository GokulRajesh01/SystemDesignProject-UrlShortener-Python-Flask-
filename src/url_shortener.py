from flask import Flask
from flask import request, redirect, jsonify
from model import InMemoryStore
import exceptions as ex

app = Flask(__name__)

# utility function to construct a url from shortcode
def construct_url(short_code):
    return f"http://localhost:5000/{short_code}"

# api endpoint to shorten a url
@app.route("/shorten", methods = ["POST"])
def shorten_url():
    req_body = request.get_json()
    if not req_body:
        return jsonify({"error": "Missing JSON request body"}), 400
    short_code = InMemoryStore.create_entry(req_body.get('long_url'))
    return construct_url(short_code), 201

# api endpoint to retrieve the long url
@app.route("/<short_code>")
def get_short_url(short_code):
    long_url = InMemoryStore.get_long_url(short_code)
    return redirect(long_url, code=302)

# Registering exceptions to be used for this flask application

@app.errorhandler(ex.EmptyLongUrlException)
@app.errorhandler(ex.EmptyShortCodeException)
@app.errorhandler(ex.InvalidCharacterInShortCode)
def handle_bad_request_exceptions(error):
    """Catches input validation errors and returns HTTP 400."""
    response = jsonify({
        "error": "Bad Request",
        "message": str(error)
    })
    return response, 400

@app.errorhandler(ex.EntryDoesNotExistException)
def handle_not_found_exceptions(error):
    """Catches lookup errors and returns HTTP 404."""
    response = jsonify({
        "error": "Not Found",
        "message": str(error)
    })
    return response, 404
if __name__ == "__main__":
    app.run(debug=True)