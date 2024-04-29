@app.route("/accounts/", methods = [ "GET" ])
def view_accounts():
	if not validate_session(session):
		destroy_session(session)
		return redirect("/login")

	page = request.args.get("page")
	per_page = request.args.get("per_page")

	if session.get("account_type") == "admin":
		accounts, page, per_page, min_page, max_page = get_data('users', page, per_page)

		return render_template(
			"account.html",
			account_type = session.get("account_type"),
			accounts = accounts,
			page = page,
			per_page = per_page,
			min_page = min_page,
			max_page = max_page
		)

	elif session.get("account_type") == "customer":
		account = get_user_info(session.get("user_id"))[0]

		account_num = get_account_num(session.get("user_id"))

		return render_template(
			"account.html",
			account_type = session.get("account_type"),
			account = account,
			account_num = account_num
		)

@app.route("/accounts/<id>")
def view_account_info(id):
	if not validate_session(session):
		destroy_session(session)
		return redirect("/login")

	account = get_user_info(id)[0]

	return render_template(
		"account_info.html",
		message = None,
		id = id,
		account_info_type = get_account_type(id),
		account_type = session.get("account_type"),
		account = account
	)

@app.route("/accounts/<id>", methods = [ "POST" ])
def approve_account(id):
	if not validate_session(session):
		destroy_session(session)
		return redirect("/login")

	# Account does not exist
	email_address = get_email_address(id)

	if not user_exists(email_address):
		return render_template(
			"account_info.html",
			message = f"User {id} does not exist",
			id = id,
			account_info_type = None,
			account_type = session.get("account_type"),
			account = None
		)

	account = get_user_info(id)[0]

	# Account already approved
	if get_account_status(id):
		return render_template(
			"account_info.html",
			message = f"User {id} is already approved",
			id = id,
			account_info_type = get_account_type(id),
			account_type = session.get("account_type"),
			account = account
		)

	# Account not approved yet
	customer_id = get_customer_id(id)

	approve_customer(customer_id)

	set_account_num(id)

	return render_template(
		"account_info.html",
		message = f"User {id} has been approved",
		id = id,
		account_info_type = get_account_type(id),
		account_type = session.get("account_type"),
		account = account
	)
