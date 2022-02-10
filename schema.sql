
CREATE TABLE users (
	 id SERIAL PRIMARY KEY,
	 username TEXT UNIQUE,
	 password TEXT,
	is_admin BOOLEAN
);


CREATE TABLE areas (
    id SERIAL PRIMARY KEY,
    content TEXT,
    user_id INTEGER REFERENCES users,
    sent_at TIMESTAMP
);

CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    content TEXT,
    user_id INTEGER REFERENCES users,
    area_id INTEGER REFERENCES areas,
    sent_at TIMESTAMP
);

CREATE TABLE reported (
    id SERIAL PRIMARY KEY,
    area_id INTEGER REFERENCES areas,
    message_id INTEGER REFERENCES messages,
    sent_at TIMESTAMP,
    area_creator_user INTEGER REFERENCES users,
    message_creator_user INTEGER REFERENCES users,
    reporter INTEGER REFERENCES users,
    report_message_content TEXT
);

