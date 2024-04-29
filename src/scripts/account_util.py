def make_transaction(account_num, amount, type, description, sender, recipient):
	if not description:
		description = "null"
	else:
		description = f"'{description}'"

	if not sender:
		sender = "null"
	else:
		sender = f"'{sender}'"

	if not recipient:
		recipient = "null"
	else:
		recipient = f"'{recipient}'"


	run_query(f"""
		insert into `transactions`
		values(
			null,
			'{account_num}',
			now(),
			{amount},
			'{type}',
			{description},
			{sender},
			{recipient}
		);
	""")

	sql.commit()

	update_balance(account_num, amount)

def update_balance(account_num, amount):
	run_query(f"""
		update `accounts`
		set `balance` = `balance` + {amount}
		where `account_num` = '{account_num}'
	""")

	sql.commit()
