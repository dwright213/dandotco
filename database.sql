-- let's set up our database

CREATE TABLE bolgs(
  id serial primary key,
  title text not null,
  body text not null
);

CREATE TABLE tags(
  id serial primary key,
  name text not null
);

CREATE TABLE bolgs_tags(
  id serial primary key,
  bolg_id int not null,
  tag_id int not null
);


-- some fixtures to keep yall dancin

INSERT INTO 
  bolgs(title, body)
VALUES 
  ('How to eat an entire can of horses in less than 10 seconds', 'Lorem Ipsum is simply dummy text of the printing and typesetting industry.'),
  ('I have decided to boycott amphibians', 'Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry'),
  ('Using Google CPC to improve brand visibility of the Lord Our God', 'Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry'),
  ('Is the x-files a real martial art?', 'Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry'),
  ('re:Backmasked messages in sports', 'Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry'),
  ('Try this one weird trick to eliminate unwanted teeth', 'Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry'),
  ('Top Ten Disappointing Video Game Novelizations', 'Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry');

