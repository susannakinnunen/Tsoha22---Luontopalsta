
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

CREATE TABLE reported_areas (
    id SERIAL PRIMARY KEY,
    area_id INTEGER REFERENCES areas,
    sent_at TIMESTAMP,
    area_creator_id INTEGER REFERENCES users,
    reporter INTEGER REFERENCES users,
    report_message_content TEXT
);

CREATE TABLE reported_messages (
	id SERIAL PRIMARY KEY,
	 message_id INTEGER REFERENCES messages,
	 area_id INTEGER REFERENCES areas,
	 sent_at TIMESTAMP,
	 message_creator_id INTEGER REFERENCES users,
	 reporter INTEGER REFERENCES users,
	 report_message_content TEXT
);
