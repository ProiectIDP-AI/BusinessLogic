from redis import Redis
import time
import os
from datetime import datetime
from flask import request, jsonify, Response, Flask
import requests
import json

app = Flask(__name__)
r = Redis(host=os.getenv('REDIS_HOST'), port=int(os.getenv('REDIS_PORT')), decode_responses=True)
url_auth = "http://auth:6000/auth/decode_token"  # Replace with your actual server URL
url_io = "http://io:5000/io"  # Replace with your actual server URL

r.set('admin_id', 0)
r.set('comp_id', 0)
r.set('emp_id', 0)
r.set('book_id', 0)
r.hset('admin', mapping={
	'id': 0,
	'name': 'admin'
})

def get_new_id(id_type: str) -> str:
	"""The function finds the next unused id and increments the global counter
	Args:
		id_type (str): The name of the type of id we want to get

	Returns:
		int: An unique ID
	"""

	new_id = id_type + '_' + str(r.incr(id_type))

	# If the id already exists, then we skip it
	while len(r.hgetall(new_id)) > 0:
		new_id = id_type + '_' + str(r.incr(id_type))

	return new_id


def decode_id(id: str) -> int:
	"""We keep the ids encoded, so that a city can have the same ID as a
		country for example, but in the database to have 2 separate keys.
		This function retrieves the number that is the ID.

	Args:
		id (str): The ID as it is in the database

	Returns:
		int: The actual ID of the entry
	"""

	return int(id.split('_')[2])


@app.route("/bl/company", methods=["POST"])
def post_comp():
	data = {
		"client_type": "admin",  # Replace with your actual client type
		"id": "None"  # Replace with your actual id or 'None'
	}

	response = requests.post(url_auth, headers=request.headers, data=json.dumps(data))
	if response.status_code != 200:
		return jsonify({'message': response.text}), 401

	payload = request.get_json()

	if not payload:
		return jsonify({'status': 'BAD REQUEST'}), 400

	if not 'name' in payload or not 'address' in payload or not 'email' \
 		or not 'comp_type' in payload:
		return jsonify({'status': 'BAD REQUEST'}), 400

	if not isinstance(payload['name'], str) or not isinstance(payload['email'], str) or \
		 not isinstance(payload['comp_type'], str) or not isinstance(payload['address'], str):

		return jsonify({'status': 'BAD REQUEST'}), 400

	url_io_company = url_io + '/company'
	response = requests.post(url_io_company, headers=request.headers, data=request.data)
	return jsonify({'message': response.text}), response.status_code


@app.route('/bl/company/<string:company_id>', methods=['GET'])
def get_company(company_id):
	data = {
		"client_type": "company",  # Replace with your actual client type
		"id": company_id  # Replace with your actual id or 'None'
	}

	response = requests.post(url_auth, headers=request.headers, data=json.dumps(data))
	if response.status_code != 200:
		return jsonify({'message': response.text}), 401

	url_io_company = url_io + '/company/' + company_id
	response = requests.get(url_io_company, headers=request.headers, data=request.data)
	return jsonify({'message': response.text}), response.status_code


# Get all companies
@app.route('/bl/company', methods=['GET'])
def get_all_companies():
	data = {
		"client_type": "admin",  # Replace with your actual client type
		"id": "None"  # Replace with your actual id or 'None'
	}

	response = requests.post(url_auth, headers=request.headers, data=json.dumps(data))
	if response.status_code != 200:
		return jsonify({'message': response.text}), 401

	url_io_company = url_io + '/company'
	response = requests.get(url_io_company, headers=request.headers, data=request.data)
	return jsonify({'message': response.text}), response.status_code


# Update company by ID
@app.route('/bl/company/<string:company_id>', methods=['PUT'])
def update_company(company_id):
	data = {
		"client_type": "admin",
		"id": "None"
	}

	response = requests.post(url_auth, headers=request.headers, data=json.dumps(data))
	if response.status_code != 200:
		return jsonify({'message': response.text}), 401

	url_io_company = url_io + '/company/' + company_id
	response = requests.put(url_io_company, headers=request.headers, data=request.data)
	return jsonify({'message': response.text}), response.status_code


# Delete company by ID
@app.route('/bl/company/<string:company_id>', methods=['DELETE'])
def delete_company(company_id):
	data = {
		"client_type": "admin",
		"id": "None"
	}

	response = requests.post(url_auth, headers=request.headers, data=json.dumps(data))
	if response.status_code != 200:
		return jsonify({'message': response.text}), 401

	url_io_company = url_io + '/company/' + company_id
	response = requests.delete(url_io_company, headers=request.headers, data=request.data)
	return jsonify({'message': response.text}), response.status_code


@app.route('/bl/admin', methods=['POST'])
def create_admin():
	data = {
		"client_type": "admin",
		"id": "None"
	}

	response = requests.post(url_auth, headers=request.headers, data=json.dumps(data))
	if response.status_code != 200:
		return jsonify({'message': response.text}), 401

	url_io_admin = url_io + '/admin'
	response = requests.post(url_io_admin, headers=request.headers, data=request.data)
	return jsonify({'message': response.text}), response.status_code


@app.route('/bl/admin/<string:id>', methods=['GET'])
def get_admin(id):
	data = {
		"client_type": "admin",
		"id": "None"
	}

	response = requests.post(url_auth, headers=request.headers, data=json.dumps(data))
	if response.status_code != 200:
		return jsonify({'message': response.text}), 401

	url_io_admin = url_io + '/admin/' + id
	response = requests.get(url_io_admin, headers=request.headers, data=request.data)
	return jsonify({'message': response.text}), response.status_code


@app.route('/bl/admin/<string:id>', methods=['PUT'])
def update_admin(id):
	data = {
		"client_type": "admin",
		"id": "None"
	}

	response = requests.post(url_auth, headers=request.headers, data=json.dumps(data))
	if response.status_code != 200:
		return jsonify({'message': response.text}), 401

	url_io_admin = url_io + '/admin/' + id
	response = requests.put(url_io_admin, headers=request.headers, data=request.data)
	return jsonify({'message': response.text}), response.status_code


@app.route('/bl/employee', methods=['POST'])
def create_employee():
	data = {
		"client_type": "company",
		"id": "None"
	}

	response = requests.post(url_auth, headers=request.headers, data=json.dumps(data))
	if response.status_code != 200:
		return jsonify({'message': response.text}), 401

	payload = request.get_json()

	if not 'first_name' in payload  \
 		or not 'last_name' in payload or not 'email' \
 		or not 'email' in payload or not 'phone_number' \
		in payload or not 'id_comp' in payload:
		return jsonify({'status': 'BAD REQUEST'}), 400

	url_io_emp = url_io + '/employee'
	response = requests.post(url_io_emp, headers=request.headers, data=request.data)
	return jsonify({'message': response.text}), response.status_code


@app.route('/bl/employee/<string:id>', methods=['GET'])
def get_employee(id):
	data = {
		"client_type": "employee",
		"id": id
	}

	response = requests.post(url_auth, headers=request.headers, data=json.dumps(data))
	if response.status_code != 200:
		return jsonify({'message': response.text}), 401

	url_io_emp = url_io + '/employee/' + id
	response = requests.get(url_io_emp, headers=request.headers, data=request.data)
	return jsonify({'message': response.text}), response.status_code


@app.route('/bl/employee', methods=['GET'])
def get_all_employees():
	data = {
		"client_type": "admin",
		"id": "None"
	}

	response = requests.post(url_auth, headers=request.headers, data=json.dumps(data))
	if response.status_code != 200:
		return jsonify({'message': response.text}), 401

	url_io_emp = url_io + '/employee'
	response = requests.get(url_io_emp, headers=request.headers, data=request.data)
	return jsonify({'message': response.text}), response.status_code


@app.route('/bl/employee/<string:id>', methods=['PUT'])
def update_employee(id):
	data = {
		"client_type": "employee",
		"id": id
	}

	response = requests.post(url_auth, headers=request.headers, data=json.dumps(data))
	if response.status_code != 200:
		return jsonify({'message': response.text}), 401

	url_io_emp = url_io + '/employee/' + id
	response = requests.put(url_io_emp, headers=request.headers, data=request.data)
	return jsonify({'message': response.text}), response.status_code


@app.route('/bl/employee/<string:id>', methods=['DELETE'])
def delete_employee(id):
	data = {
		"client_type": "employee",
		"id": id
	}

	response = requests.post(url_auth, headers=request.headers, data=json.dumps(data))
	if response.status_code != 200:
		return jsonify({'message': response.text}), 401

	url_io_emp = url_io + '/employee/' + id
	response = requests.delete(url_io_emp, headers=request.headers, data=request.data)
	return jsonify({'message': response.text}), response.status_code


@app.route('/bl/employee/<string:id>/books/active', methods=['POST'])
def add_active_book(id):
	data = {
		"client_type": "employee_only",
		"id": id
	}

	response = requests.post(url_auth, headers=request.headers, data=json.dumps(data))
	if response.status_code != 200:
		return jsonify({'message': response.text}), 401

	url_io_emp = url_io + '/employee/' + id + '/books/active'
	response = requests.post(url_io_emp, headers=request.headers, data=request.data)
	return jsonify({'message': response.text}), response.status_code



@app.route('/bl/employee/<string:id>/books/wishlist', methods=['POST'])
def add_wishlist_book(id):
	data = {
		"client_type": "employee_only",
		"id": id
	}

	response = requests.post(url_auth, headers=request.headers, data=json.dumps(data))
	if response.status_code != 200:
		return jsonify({'message': response.text}), 401

	url_io_emp = url_io + '/employee/' + id + '/books/wishlist'
	response = requests.post(url_io_emp, headers=request.headers, data=request.data)
	return jsonify({'message': response.text}), response.status_code


@app.route('/bl/employee/<string:id>/books/listened', methods=['POST'])
def add_listened_book(id):
	data = {
		"client_type": "employee_only",
		"id": id
	}

	response = requests.post(url_auth, headers=request.headers, data=json.dumps(data))
	if response.status_code != 200:
		return jsonify({'message': response.text}), 401

	url_io_emp = url_io + '/employee/' + id + '/books/listened'
	response = requests.post(url_io_emp, headers=request.headers, data=request.data)
	return jsonify({'message': response.text}), response.status_code


@app.route('/bl/employee/<string:id>/books', methods=['GET'])
def get_employee_books(id):
	data = {
		"client_type": "employee",
		"id": id
	}

	response = requests.post(url_auth, headers=request.headers, data=json.dumps(data))
	if response.status_code != 200:
		return jsonify({'message': response.text}), 401

	url_io_emp = url_io + '/employee/' + id + '/books'
	response = requests.get(url_io_emp, headers=request.headers, data=request.data)
	return jsonify({'message': response.text}), response.status_code



@app.route('/bl/employee/<string:id>/books/active', methods=['DELETE'])
def delete_active_book(id):
	data = {
		"client_type": "employee_only",
		"id": id
	}

	response = requests.post(url_auth, headers=request.headers, data=json.dumps(data))
	if response.status_code != 200:
		return jsonify({'message': response.text}), 401

	url_io_emp = url_io + '/employee/' + id + '/books/active'
	response = requests.delete(url_io_emp, headers=request.headers, data=request.data)
	return jsonify({'message': response.text}), response.status_code


@app.route('/bl/employee/<string:id>/books/wishlist', methods=['DELETE'])
def delete_wishlist_book(id):
	data = {
		"client_type": "employee_only",
		"id": id
	}

	response = requests.post(url_auth, headers=request.headers, data=json.dumps(data))
	if response.status_code != 200:
		return jsonify({'message': response.text}), 401

	url_io_emp = url_io + '/employee/' + id + '/books/wishlist'
	response = requests.delete(url_io_emp, headers=request.headers, data=request.data)
	return jsonify({'message': response.text}), response.status_code

@app.route('/bl/employee/<string:id>/books/listened', methods=['DELETE'])
def delete_listened_book(id):
	data = {
		"client_type": "employee_only",
		"id": id
	}

	response = requests.post(url_auth, headers=request.headers, data=json.dumps(data))
	if response.status_code != 200:
		return jsonify({'message': response.text}), 401

	url_io_emp = url_io + '/employee/' + id + '/books/listened'
	response = requests.delete(url_io_emp, headers=request.headers, data=request.data)
	return jsonify({'message': response.text}), response.status_code

@app.route("/bl/book", methods=["POST"])
def post_book():
	payload = request.get_json()

	if not payload:
		return jsonify({'status': 'BAD REQUEST'}), 400

	if not 'name' in payload or not 'author' in payload or not 'length' in payload \
		or not 'publish_date' in payload or not 'description' in payload \
		or not 'book_type' in payload or not 'link' in payload:
		return jsonify({'status': 'BAD REQUEST'}), 400

	if not isinstance(payload['name'], str) or not isinstance(payload['author'], str) \
		or not isinstance(payload['length'], str) or not isinstance(payload['publish_date'], str) \
		or not isinstance(payload['description'], str) or not isinstance(payload['book_type'], str) \
		or not isinstance(payload['link'], str):
		return jsonify({'status': 'BAD REQUEST'}), 400

	data = {
		"client_type": "admin",
		"id": "None"
	}

	response = requests.post(url_auth, headers=request.headers, data=json.dumps(data))
	if response.status_code != 200:
		return jsonify({'message': response.text}), 401

	url_io_book = url_io + '/book'
	response = requests.post(url_io_book, headers=request.headers, data=request.data)
	return jsonify({'message': response.text}), response.status_code


@app.route('/bl/book/<string:book_id>', methods=['GET'])
def get_book(book_id):
	data = {
		"client_type": "all",
		"id": "None"
	}

	response = requests.post(url_auth, headers=request.headers, data=json.dumps(data))
	if response.status_code != 200:
		return jsonify({'message': response.text}), 401

	url_io_book = url_io + '/book/' + book_id
	response = requests.get(url_io_book, headers=request.headers, data=request.data)
	return jsonify({'message': response.text}), response.status_code


@app.route('/bl/book', methods=['GET'])
def get_all_books():
	data = {
		"client_type": "all",
		"id": "None"
	}

	response = requests.post(url_auth, headers=request.headers, data=json.dumps(data))
	if response.status_code != 200:
		return jsonify({'message': response.text}), 401

	url_io_book = url_io + '/book'
	response = requests.get(url_io_book, headers=request.headers, data=request.data)
	return jsonify({'message': response.text}), response.status_code


@app.route('/bl/book/<string:book_id>', methods=['PUT'])
def update_book(book_id):
	data = {
		"client_type": "admin",
		"id": "None"
	}

	response = requests.post(url_auth, headers=request.headers, data=json.dumps(data))
	if response.status_code != 200:
		return jsonify({'message': response.text}), 401

	url_io_book = url_io + '/book/' + book_id
	response = requests.put(url_io_book, headers=request.headers, data=request.data)
	return jsonify({'message': response.text}), response.status_code



@app.route('/bl/book/<string:book_id>', methods=['DELETE'])
def delete_book(book_id):
	data = {
		"client_type": "admin",
		"id": "None"
	}

	response = requests.post(url_auth, headers=request.headers, data=json.dumps(data))
	if response.status_code != 200:
		return jsonify({'message': response.text}), 401

	url_io_book = url_io + '/book/' + book_id
	response = requests.delete(url_io_book, headers=request.headers, data=request.data)
	return jsonify({'message': response.text}), response.status_code


if __name__ == '__main__':
   app.run('0.0.0.0', port=7000, debug=True)
