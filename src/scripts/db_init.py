run_file("./db/drop.sql")
run_file("./db/tables.sql")

run_query("""
	insert into `users` values
	(
		NULL,
		'admin',
		'Admin',
		'Account',
		'1234567890',
		'a@a.a',
		'1234567890',
		'ca978112ca1bbdcafac231b39a23dc4da786eff8147c4e72b9807785afee48bb'
	);
""")

run_query("""
	insert into `admins` values
	(
		NULL,
		1
	);
""")

run_query("""
	insert into `users` values
	(
		NULL,
		'customer',
		'Customer',
		'Account',
		'1234567890',
		'c@c.c',
		'1234567890',
		'2e7d2c03a9507ae265ecf5b5356885a53393a2029d241394997265a1a25aefc6'
	);
""")

run_query("""
	insert into `customers` values
	(
		NULL,
		2,
		0
	);
""")

sql.commit()
