drop table if exists match;
CREATE TABLE match (
  id integer primary key autoincrement,
  active boolean NOT NULL, -- if the match is the current one
  user_id_1 integer NOT NULL,
  user_id_2 integer NOT NULL,
  timestarted integer, -- Handle timestamp else where
  score integer,
  winner integer,
  FOREIGN KEY(user_id_1) REFERENCES users,
  FOREIGN KEY(user_id_2) REFERENCES users
);

drop view if exists match_data;
CREATE VIEW match_data AS SELECT
    match.active,
    match.winner,
    match.id,
    match.timestarted,
    match.user_id_1,
    match.user_id_2,
    user1.username AS username1,
    user2.username AS username2
FROM match
    LEFT JOIN users user1 ON match.user_id_1=user1.id
    LEFT JOIN users user2 ON match.user_id_2=user2.id;

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
  -- snap_shot_name text primary key,
  description text,
  category_id integer,
  flag text,
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
