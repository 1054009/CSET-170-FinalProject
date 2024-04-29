@app.route("/transactions/add")
def view_deposit_form():
	return render_template("card_input.html")

@app.route("/transactions/add", methods = [ "POST" ])
def deposit():
	return render_template("card_input.html", message = "Deposited")
