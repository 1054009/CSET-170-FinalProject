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
		account = get_query_rows(f"""
			select * from `users`
			where `id` = {session.get("user_id")}
		""")

		return render_template(
			"account.html",
			account_type = session.get("account_type"),
			account = account
		)
