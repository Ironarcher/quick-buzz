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
	name text not null
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
	categorytype text,
	name text not null
);

insert into users (username, password, email) values ("admin", "code_39A$NPQ", "arpad.kovesdy@gmail.com");