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

def account_exists(account_num):
	"""
	:param str account_num:

	:return:
		1 if the account_num exists in accounts table

		0 otherwise

	:rtype: int
	"""

	return get_query_rows(f"""
		select exists
			(
				select `account_num`
				from `accounts`
				where `account_num` = '{account_num}'
			) as `exists`;
	""")[0].exists
