create table `users`
(
	`id` int unsigned auto_increment,
	`username` varchar(64) not null,
	`first_name` varchar(64) not null,
	`last_name` varchar(64) not null,
	`ssn` varchar(11) not null,
	`email_address` varchar(64) unique not null,
	`phone_number` varchar(15) not null,
	`password` blob not null,

	primary key (`id`)
);

create table `admins`
(
	`id` int unsigned auto_increment,
	`user_id` int unsigned not null,

	primary key (`id`),
	foreign key (`user_id`) references `users` (`id`) on delete cascade on update restrict
);

create table `customers`
(
	`id` int unsigned auto_increment,
	`user_id` int unsigned not null,
	`is_approved` boolean not null,

	primary key (`id`),
	foreign key (`user_id`) references `users` (`id`) on delete cascade on update restrict
);

create table `accounts`
(
	`id` int unsigned auto_increment,
	`account_num` varchar(10) not null,
	`user_id` int unsigned not null,
	`balance` float(23, 2) default 0.00,

	primary key (`id`),
	foreign key (`user_id`) references `users` (`id`) on delete cascade on update restrict,
	unique (`account_num`)
);

create table `transactions`
(
	`id` int unsigned auto_increment,
	`account_num` varchar(10) not null,
	`time` datetime not null,
	`amount` float(23, 2) not null,
	`transaction_type` enum("added", "sent", "received") not null,
	`description` varchar(255),
	`sender` varchar(10),
	`recipient` varchar(64),
	`new_balance` float(23,2) default 0.00

	primary key (`id`),
	foreign key (`account_num`) references `accounts` (`account_num`) on delete cascade on update restrict
);
