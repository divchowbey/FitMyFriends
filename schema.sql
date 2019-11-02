CREATE TABLE user (
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  email TEXT UNIQUE NOT NULL,
  profile_pic TEXT NOT NULL,
  phone TEXT
);

CREATE TABLE friend(
  friend_id TEXT PRIMARY KEY,
  user_id TEXT NOT NULL,
  friend_user_id TEXT NOT NULL,
  friend_name TEXT NOT NULL,
  friend_email TEXT UNIQUE NOT NULL,
  friend_phone TEXT,
  FOREIGN KEY(user_id) REFERENCES user(id),
  FOREIGN KEY(friend_user_id) REFERENCES user(id),
  FOREIGN KEY(friend_name) REFERENCES user(name),
  FOREIGN KEY(friend_email) REFERENCES user(email),
  FOREIGN KEY(friend_phone) REFERENCES user(phone)
);

CREATE TABLE exercise(
  exercise_id TEXT PRIMARY KEY,
  user_id TEXT NOT NULL,
  friend_id TEXT,
  date_time datetime default current_timestamp,
  exercise_type TEXT
);
