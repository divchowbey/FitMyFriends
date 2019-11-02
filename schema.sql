CREATE TABLE user (
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  email TEXT UNIQUE NOT NULL,
  profile_pic TEXT NOT NULL
);

CREATE TABLE friend(
  friend_id TEXT PRIMARY KEY,
  user_id TEXT NOT NULL,
  friend_user_id TEXT NOT NULL,
  FOREIGN KEY(user_id) REFERENCES user(id),
  FOREIGN KEY(friend_user_id) REFERENCES user(id)
);

CREATE TABLE exercise(
  exercise_id TEXT PRIMARY KEY,
  user_id TEXT NOT NULL,
  friend_id TEXT,
  date_time datetime default current_timestamp,
  exercise_type TEXT
);
