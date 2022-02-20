
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
    sent_at TIMESTAMP,
    visible BOOLEAN
);

CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    content TEXT,
    user_id INTEGER REFERENCES users,
    area_id INTEGER REFERENCES areas,
    sent_at TIMESTAMP,
    visible BOOLEAN,
    image_id INTEGER REFERENCES images
);

CREATE TABLE reported_areas (
    id SERIAL PRIMARY KEY,
    area_id INTEGER REFERENCES areas,
    sent_at TIMESTAMP,
    area_creator_id INTEGER REFERENCES users,
    reporter INTEGER REFERENCES users,
    report_message_content TEXT
    area_created_at TIMESTAMP REFERENCES areas
);

CREATE TABLE reported_messages (
	id SERIAL PRIMARY KEY,
	 message_id INTEGER REFERENCES messages,
	 area_id INTEGER REFERENCES areas,
	 sent_at TIMESTAMP,
	 message_creator_id INTEGER REFERENCES users,
	 reporter INTEGER REFERENCES users,
	 report_message_content TEXT,
	 org_message_sent_at TIMESTAMP REFERENCES messages
);

CREATE TABLE observation_info (
	id SERIAL PRIMARY KEY,
	day DATE,
	time TIME WITHOUT TIME ZONE,
	message_id INTEGER REFERENCES messages,
	location TEXT
);

CREATE TABLE images (
	id SERIAL PRIMARY KEY,
	name TEXT,
	data BYTEA,
	message_id INTEGER REFERENCES messages
);
	
	
