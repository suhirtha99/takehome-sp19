from typing import Tuple

from flask import Flask, jsonify, request, Response
import mockdb.mockdb_interface as db

app = Flask(__name__)


def create_response(
    data: dict = None, status: int = 200, message: str = ""
) -> Tuple[Response, int]:
    """Wraps response in a consistent format throughout the API.
    
    Format inspired by https://medium.com/@shazow/how-i-design-json-api-responses-71900f00f2db
    Modifications included:
    - make success a boolean since there's only 2 values
    - make message a single string since we will only use one message per response
    IMPORTANT: data must be a dictionary where:
    - the key is the name of the type of data
    - the value is the data itself

    :param data <str> optional data
    :param status <int> optional status code, defaults to 200
    :param message <str> optional message
    :returns tuple of Flask Response and int, which is what flask expects for a response
    """
    if type(data) is not dict and data is not None:
        raise TypeError("Data should be a dictionary 😞")

    response = {
        "code": status,
        "success": 200 <= status < 300,
        "message": message,
        "result": data,
    }
    return jsonify(response), status


"""
~~~~~~~~~~~~ API ~~~~~~~~~~~~
"""


@app.route("/")
def hello_world():
    return create_response({"content": "hello world!"})


@app.route("/mirror/<name>")
def mirror(name):
    data = {"name": name}
    return create_response(data)


@app.route("/shows", methods=['GET'])
def get_all_shows():
    # Part 3: query string for minEpisodes
    if (request.args.get('minEpisodes') != None):
        minEpisodes = request.args.get('minEpisodes')
        to_return = []
        for show in db.get('shows'):
            if show["episodes_seen"] >= int(minEpisodes):
                to_return.append(show)
        return create_response({"shows": to_return})
    else:
        return create_response({"shows": db.get('shows')})

@app.route("/shows/<id>", methods=['DELETE'])
def delete_show(id):
    if db.getById('shows', int(id)) is None:
        return create_response(status=404, message="No show with this id exists")
    db.deleteById('shows', int(id))
    return create_response(message="Show deleted")


# TODO: Implement the rest of the API here!

# Part 2 --> define the endpoint GET /shows/<id>
@app.route("/shows/<id>", methods=['GET'])
def get_show_by_id(id):
    if db.getById('shows', int(id)) is None:
        return create_response(status=404, message="No show with this id exists.")
    return create_response({"shows": db.getById('shows', int(id))})


# Part 4 --> define the endpoint POST /shows
# created using 'name' and 'episodes_seen'
# returns added show
@app.route("/shows", methods=['POST'])
def add_show():
    new_show_data = request.get_json()
    if 'name' not in new_show_data or 'episodes_seen' not in new_show_data:
        return create_response(status=422, message="Please include the name and episodes seen for the show you are trying to add.")
    new_show = db.create('shows', new_show_data)
    return create_response({"added_show": new_show})

# Part 5 --> define the endpoint PUT /shows/<id>
# updated using params (name, episodes_seen)
# returns updated show
@app.route("/shows/<id>", methods=['PUT'])
def update_show(id):
    new_data = request.get_json()
    if 'name' not in new_data and 'episodes_seen' not in new_data:
        return create_response(status=422, message="Please include the name or episodes seen for the show you are trying to update.")
    updated_show = db.updateById('shows', int(id), new_data)
    return create_response({"updated_show": updated_show})


"""
~~~~~~~~~~~~ END API ~~~~~~~~~~~~
"""
if __name__ == "__main__":
    app.run(port=8080, debug=True)
