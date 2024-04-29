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

	make_transaction(session.get("account_num"), amount, "added", description, "", "")

	return render_template(
		"card_input.html",
		message = f"${pricefy(amount)} deposited",
		card_number = session.get("card_number"),
		expiration_date = session.get("expiration_date"),
		ccv = session.get("ccv")
	)

@app.route("/transactions/send")
def view_transaction_send_form():
	if not validate_session(session):
		destroy_session(session)
		return redirect("/login")

	return render_template("transaction_send.html")

@app.route("/transactions/send", methods = [ "POST" ])
def send_money():
	if not validate_session(session):
		destroy_session(session)
		return redirect("/login")

	# Get data from form
	receiver_account_num = request.form.get("receiver_account_num")
	amount = float(request.form.get("amount"))
	description = request.form.get("description")

	# Check if receiver account number exists in accounts table
	if not account_exists(receiver_account_num):
		return render_template(
			"transaction_send.html",
			message = f"Account {receiver_account_num} does not exist"
		)

	# Check if sending to self
	sender_account_num = session.get("account_num")

	if receiver_account_num == sender_account_num:
		return render_template(
			"transaction_send.html",
			message = f"You cannot send money to yourself. Please deposit money"
		)

	# Check if there is sufficient balance
	sender_account_balance = get_account_balance(sender_account_num)

	if sender_account_balance < amount:
		return render_template(
			"transaction_send.html",
			message = f"You do not have enough balance for this transaction. Your balance is ${pricefy(sender_account_balance)}"
		)

	# Sender transaction
	make_transaction(sender_account_num, -amount, "sent", description, "", receiver_account_num)

	# Receiver transaction
	make_transaction(receiver_account_num, amount, "received", description, sender_account_num, "")

	return render_template(
		"transaction_send.html",
		message = f"${pricefy(amount)} has been transferred to {receiver_account_num}"
	)
