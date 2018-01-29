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

drop table if exists users;
CREATE TABLE users(
  id integer primary key autoincrement,
  username text NOT NULL UNIQUE,
  score integer DEFAULT 0,
  current_flag text,
  next_score integer DEFAULT 50,
  avatar_id integer,
  FOREIGN KEY(avatar_id) REFERENCES AVATAR
);

drop table if exists avatars;
CREATE TABLE avatars (
  id integer primary key autoincrement,
  name text,
  sprite_sheet_name text,
  hero_image text
);

INSERT INTO avatars (name, sprite_sheet_name, hero_image)
VALUES ("RYU", "ryu.gif", "ryu_hero.png");


drop table if exists challenge_catogory;
create table challenge_catogory(
  id integer primary key autoincrement,
  label text,
  description text
);

drop table if exists challenge;
create table challenge (
  domain text,
  snapshot text,
  description text,
  category text,
  category_id integer,
  difficulty integer,
  flag text,
  score integer DEFAULT 50,
  FOREIGN KEY(category_id) REFERENCES challenge_catogory,
  PRIMARY KEY(domain, snapshot)
);

drop table if exists domain_snapshot;
create table domain_snapshot (
  snapshot_id integer,
  domain_id integer,
  FOREIGN KEY(snapshot_id) REFERENCES snapshot,
  FOREIGN KEY(domain_id) REFERENCES domain,
  PRIMARY KEY(domain_id, snapshot_id)
);

drop table if exists snapshot;
create table snapshot (
  id integer primary key autoincrement,
  name text NOT NULL UNIQUE
);

drop table if exists domain;
create table domain (
  id integer primary key autoincrement,
  name text NOT NULL UNIQUE
);

drop table if exists admin;
create table admin(
  id integer primary key  autoincrement
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

drop view if exists vm_data;
CREATE VIEW vm_data AS SELECT
    snapshot.name AS snapshot_name,
    domain.name AS domain_name,
    snapshot.id AS snapshot_id,
    domain.id AS domain_id
FROM snapshot, domain, domain_snapshot
WHERE snapshot_id = domain_snapshot.snapshot_id and domain_id = domain_snapshot.domain_id;
