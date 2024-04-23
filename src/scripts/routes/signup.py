@app.route("/signup/", methods = [ "GET", "POST" ])
def signup():
	destroy_session(session) # Log them out

	if request.method == "POST":
		# No input sanitization? Rock on!
		email_address = request.form.get("email_address")
		password = request.form.get("password") # Not encrypted during transit oh well
		password_verify = request.form.get("password_verify")

		if password != password_verify:
			return render_template(
				"signup.html",
				no_navbar = True,
				error = "Passwords don't match"
			)

		if user_exists(email_address):
			return render_template(
				"signup.html",
				no_navbar = True,
				error = "A user with this email already exists!"
			)

		try:
			run_query(
				"insert into `users` values ( NULL, :first_name, :last_name, :username, :ssn, :email_address, :phone_number, :password )",

				{
					"first_name": request.form.get("first_name"),
					"last_name": request.form.get("last_name"),
					"username": request.form.get("username"),
					"ssn": request.form.get("ssn"),
					"email_address": email_address,
					"phone_number": request.form.get("phone_number"),
					"password": sha_string(password),
				}
			)


			run_query(f"insert into `customers` values ( NULL, {user_exists(email_address)}, 0 )")

			sql.commit()

			return redirect("/login")
		except:
			return render_template(
				"signup.html",
				no_navbar = True,
				error = "Failed to create account. Contact an administrator."
			)
	else:
		return render_template("signup.html", no_navbar = True)
