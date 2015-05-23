drop table if exists entries;
drop table if exists users;
drop table if exists lobbies;
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

create table lobbies (
	id integer primary key autoincrement,
	name text not null
);