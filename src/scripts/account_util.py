def make_transaction(account_id, amount, type, description, recipient):
	if not description:
		description = "null"
	else:
		description = f"'{description}'"

	if not recipient:
		recipient = "null"
	else:
		recipient = f"'{recipient}'"

	run_query(f"""
		insert into `transactions`
		values(
			null,
			'{account_id}',
			now(),
			{amount},
			'{type}',
			{description},
			{recipient}
		);
	""")

	sql.commit()

def update_balance(account_num, amount):
	run_query(f"""
		update `accounts`
		set `balance` += {amount}
		where `account_num` = {account_num}
	""")

	sql.commit()
