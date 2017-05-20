drop table if exists match;
CREATE TABLE match (
  id integer primary key autoincrement,
  active boolean NOT NULL, -- if the match is the current one
  user_id_1 integer NOT NULL,
  user_id_2 integer NOT NULL,
  timestarted integer, -- Handle timestamp else where
  score integer,
  winner integer,
  FOREIGN KEY(user_id_1) REFERENCES user,
  FOREIGN KEY(user_id_2) REFERENCES user
);

drop table if exists user;
CREATE TABLE user(
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

create table domain_snapshot (
  snapshot_id integer,
  domain_id integer,
  FOREIGN KEY(snapshot_id) REFERENCES snapshot,
  FOREIGN KEY(domain_id) REFERENCES domain,
  PRIMARY KEY(domain_id, snapshot_id)
);

create table snapshot (
  id integer primary key autoincrement,
  name text NOT NULL UNIQUE
);

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
    LEFT JOIN user user1 ON match.user_id_1=user1.id
    LEFT JOIN user user2 ON match.user_id_2=user2.id;

drop view if exists vm_data;
CREATE VIEW vm_data AS SELECT
    snapshot.name AS snapshot_name,
    domain.name AS domain_name,
    snapshot.id AS snapshot_id,
    domain.id AS domain_id
FROM snapshot, domain, domain_snapshot
WHERE snapshot_id = domain_snapshot.snapshot_id and domain_id = domain_snapshot.domain_id;
