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

	new_balance = get_account_balance(account_num) + float(amount)

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
			{recipient},
			{new_balance}
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

def get_account_balance(account_num):
	"""
	:param str account_num:

	:return:
		The balance if the account exists

		False otherwise

	:rtype:
		float if the account exists

		boolean otherwise
	"""

	if not account_exists(account_num):
		return False

	return float(get_query_rows(f"""
		select `balance`
		from `accounts`
		where `account_num` = '{account_num}';
	""")[0].balance)
