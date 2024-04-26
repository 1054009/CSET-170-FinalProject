def sha_string(string):
	return hashlib.sha256(string.encode("utf-8")).hexdigest()

def user_exists(email_address):
	"""
	:param str email_address: The email associated with a user

	:return:
		The user id if the user account exists

		False otherwise

	:rtype:
		int if the email exists

		bool otherwise

	"""
	user = get_query_rows(f"select * from `users` where `email_address` = '{email_address}'")

	if len(user) < 1:
		return False

	return user[0].id

def get_admin_id(user_id):
	"""
	:param int user_id:

	:return:
		The admin id if the admin account exists

		False otherwise
	:rtype:
		int if the user_id exists

		bool otherwise
	"""

	admin = get_query_rows(f"select * from `admins` where `user_id` = {user_id}")

	if len(admin) < 1:
		return False

	return admin[0].id

def get_customer_id(user_id):
	"""
	:param int user_id:

	:return:
		The customer id if the customer account exists

		False otherwise

	:rtype:
		int if the user_id exists

		bool otherwise
	"""

	customer = get_query_rows(f"select * from `customers` where `user_id` = {user_id}")

	if len(customer) < 1:
		return False

	return customer[0].id

def get_account_type(user_id):
	"""
	:param int user_id:

	:return:
		"admin" if the account type is admin

		"customer" if the account type is customer

		False otherwise

	:rtype:
		str if the account exists

		bool otherwise
	"""

	if get_admin_id(user_id):
		return "admin"

	if get_customer_id(user_id):
		return "customer"

	return False

def get_account_status(user_id):
	"""
	:param int user_id:

	:return:

		1 if the account is approved

		0 if the account is not approved

		False if the account doesn't exist

	:rtype:
		int if the account exists

		bool otherwise
	"""

	status = get_query_rows(f"select `is_approved` from `customers` where `user_id` = {user_id}")

	if len(status) < 1:
		return False

	return status[0].is_approved

def get_user_info(user_id):
	return get_query_rows(f"""
		select * from `users`
		where `id` = {user_id}
	""")

def validate_login(email_address, password):
	"""
	:param str email_address:
	:param str password:

	:return:
		True if the hashed password matches the stored hashed password

		False otherwise

	:rtype: bool
	"""
	if not user_exists(email_address):
		return False

	stored_password = get_query_rows(f"select `password` from `users` where `email_address` = '{email_address}'")

	if len(stored_password) < 1:
		return False

	stored_password = stored_password[0].password
	stored_password = stored_password.decode("utf-8")

	return sha_string(password) == stored_password

def destroy_session(session):
	if not session:
		return

	if session.get("user_id"): del session["user_id"]
	if session.get("email_address"): del session["email_address"]

def validate_session(session):
	if not session:
		return False

	user_id = session.get("user_id")
	email_address = session.get("email_address")

	if not user_id or not email_address:
		return False

	return user_id == user_exists(email_address)
