-- clean and set up database


DROP TABLE IF EXISTS bolg, tag, bolgs_tags;

CREATE TABLE bolg(
  id serial primary key,
  title text not null,
  perma text not null,
  excerpt text,
  body text,
  body_src text not null,
  created date not null,
  images JSON,
  kind text
);

CREATE TABLE tag(
  id serial primary key,
  name text not null
);

CREATE TABLE bolgs_tags(
  id serial primary key,
  bolg_id int not null,
  tag_id int not null
);

