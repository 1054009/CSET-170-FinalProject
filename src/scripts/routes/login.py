@app.route("/login/", methods = [ "GET", "POST" ])
def login():
	destroy_session(session)

	if request.method == "POST":
		email_address = request.form.get("email_address")
		password = request.form.get("password")
		user_id = user_exists(email_address)

		if not user_id:
			return render_template(
				"login.html",
				no_navbar = True,
				error = "A user with this email does not exist"
			)

		if validate_login(email_address, password):
			account_type = get_account_type(user_id)

			if not get_account_status(user_id) and account_type == "customer":
				return render_template(
				"login.html",
				no_navbar = True,
				error = "Your account has not been approved yet"
			)
			session["user_id"] = user_id
			session["email_address"] = email_address

			session["account_type"] = account_type

			session["admin_id"] = get_admin_id(user_id)
			session["customer_id"] = get_customer_id(user_id)

			session["is_approved"] = get_account_status(user_id)

			return redirect("/home")
		else:
			return render_template(
				"login.html",
				no_navbar = True,
				error = "Invalid password"
			)
	else:
		return render_template("login.html", no_navbar = True)
