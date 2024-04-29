@app.route("/transactions/add")
def view_deposit_form():
	if not validate_session(session):
		destroy_session(session)
		return redirect("/login")

	return render_template("card_input.html")

@app.route("/transactions/add", methods = [ "POST" ])
def deposit():
	if not validate_session(session):
		destroy_session(session)
		return redirect("/login")

	# Get data from form
	card_number = request.form.get("card_number")
	expiration_date = request.form.get("expiration_date")
	ccv = request.form.get("ccv")
	amount = request.form.get("amount")
	description = request.form.get("description")

	# Save card info
	session["card_number"] = card_number
	session["expiration_date"] = expiration_date
	session["ccv"] = ccv

	# Add transaction
	session["account_num"] = get_account_num(session.get("user_id"))

	make_transaction(session.get("account_num"), amount, "added", description, "")

	return render_template(
		"card_input.html",
		message = f"${amount} deposited",
		card_number = session.get("card_number"),
		expiration_date = session.get("expiration_date"),
		ccv = session.get("ccv")
	)
