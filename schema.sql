drop table if exists users;

CREATE TABLE users(
  id integer primary key autoincrement,
  username text NOT NULL UNIQUE,
  score integer DEFAULT 0,
  current_flag text,
  next_score integer DEFAULT 50
);

drop table if exists challenge_catogory;
create table challenge_catogory(
  id integer primary key autoincrement,
  label text,
  description text
);

drop table if exists challenge;
create table challenge (
  id integer primary key autoincrement,
  short_name text,
  description text,
  category_id integer,
  FOREIGN KEY(category_id) REFERENCES challenge_catogory
);

drop table if exists flags;
create table flags (
  challenge_id integer,
  user_id integer,
  flag text NOT NULL,

  PRIMARY KEY (user_id, challenge_id),
  FOREIGN KEY(user_id) REFERENCES users(id),
  FOREIGN KEY(challenge_id) REFERENCES challenge(id)
);

drop table if exists admin;
create table admin(
  id integer primary key  autoincrement
);
