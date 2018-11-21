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
  images JSON
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


-- -- some fixtures to keep yall dancin
-- INSERT INTO 
--   bolg(title, body, created)
-- VALUES 
--   ('How to eat an entire can of horses in less than 10 seconds', 
--     'Lorem Ipsum is simply dummy text of the printing and typesetting industry.', 
--     '2015-12-17'),
--   ('I have decided to boycott amphibians', 
--     'Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry', 
--     '2015-12-18'),
--   ('Using Google CPC to improve brand visibility of the Lord Our God', 
--     'Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry', 
--     '2015-12-19'),
--   ('Is the x-files a real martial art?', 
--     'Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry', 
--     '2015-12-20'),
--   ('re:Backmasked messages in sports', 
--     'Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry', 
--     '2015-12-21'),
--   ('Try this one weird trick to eliminate unwanted teeth', 
--     'Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry', 
--     '2015-12-22'),
--   ('Top Ten Disappointing Video Game Novelizations', 
--     'Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry', 
--     '2015-12-23');

-- INSERT INTO
--   tag(name) 
-- VALUES
--   ('tupac'),
--   ('nas'),
--   ('rockness monster'),
--   ('booyaa tribe'),
--   ('myka 9'),
--   ('jeru the damaja'),
--   ('kmd');

--   INSERT INTO
--     bolgs_tags(bolg_id, tag_id)
--   VALUES 
--     (1,1),
--     (1,2),
--     (1,3),
    
--     (2,3),
--     (2,6),
--     (2,5),

--     (3,1),
--     (3,2),
--     (3,3),

--     (4,1),
--     (4,2),
--     (4,3),

--     (5,4),
--     (5,5),
--     (5,6),

--     (6,2),
--     (6,3),
--     (6,4),

--     (7,3),
--     (7,4),
--     (7,5);

