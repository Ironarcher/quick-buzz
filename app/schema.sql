drop table if exists entries;
drop table if exists users;
drop table if exists friends;
drop table if exists lobbies;
drop table if exists questions;
drop table if exists sets;

create table entries (
	id integer primary key autoincrement,
	title text not null,
	text text not null
);

create table users (
	id integer primary key autoincrement,
	username text not null,
	firstname text,
	lastname text,
	password text not null,
	email text not null
);

create table friends (
	frienderId integer references user(id),
	friendedId integer references user(id)
);

create table lobbies (
	id integer primary key autoincrement,
	name text not null,
	player1in boolean default false,
	player2in boolean default false,
	player3in boolean default false,
	player4in boolean default false,
	player5in boolean default false,
	player6in boolean default false,
	player7in boolean default false,
	player8in boolean default false,
	player9in boolean default false,
	player10in boolean default false,
	player1id integer references user(id),
	player2id integer references user(id),
	player3id integer references user(id),
	player4id integer references user(id),
	player5id integer references user(id),
	player6id integer references user(id),
	player7id integer references user(id),
	player8id integer references user(id),
	player9id integer references user(id),
	player10id integer references user(id),
	player1pts integer default 0,
	player2pts integer default 0,
	player3pts integer default 0,
	player4pts integer default 0,
	player5pts integer default 0,
	player6pts integer default 0,
	player7pts integer default 0,
	player8pts integer default 0,
	player9pts integer default 0,
	player10pts integer default 0,
	setid integer references sets(id),
	questionposition integer default 0,
	unixtimer integer default 0,
	status text not null
);

create table questions (
	id integer primary key autoincrement,
	creatorId integer references user(id),
	question text not null,
	answer text not null,
	rating integer default 0,
	timeallowed integer default 15,
	datecreated integer not null,
	ownerset text references sets(id)
);

create table sets (
	id integer primary key autoincrement,
	creatorId integer references user(id),
	isPublic boolean,
	categorytype tex,
	name text not null
);

insert into users (username, password, email) values ("admin", "code_39A$NPQ", "arpad.kovesdy@gmail.com");