
CREATE TABLE addresses (
	id INTEGER NOT NULL,
	city VARCHAR,
	zipcode VARCHAR,
	number VARCHAR,
	street VARCHAR,
	country VARCHAR,
	PRIMARY KEY (id)
)

;


CREATE TABLE banned_users (
	id INTEGER NOT NULL,
	banned_email VARCHAR NOT NULL,
	banned_by_email VARCHAR,
	banned_at DATETIME,
	PRIMARY KEY (id),
	UNIQUE (banned_email)
)

;


CREATE TABLE failed_logins (
	id INTEGER NOT NULL,
	ip_address VARCHAR,
	attempts INTEGER,
	last_attempt DATETIME,
	PRIMARY KEY (id)
)

;


CREATE TABLE reasons (
	id INTEGER NOT NULL,
	reason VARCHAR NOT NULL,
	PRIMARY KEY (id),
	UNIQUE (reason)
)

;


CREATE TABLE roles (
	id INTEGER NOT NULL,
	role VARCHAR,
	PRIMARY KEY (id)
)

;


CREATE TABLE types (
	id INTEGER NOT NULL,
	type VARCHAR,
	PRIMARY KEY (id)
)

;


CREATE TABLE users (
	id INTEGER NOT NULL,
	email VARCHAR,
	password VARCHAR,
	phone_number VARCHAR,
	is_planner BOOLEAN,
	created_at DATETIME,
	role_id INTEGER,
	account_id VARCHAR,
	is_verified BOOLEAN,
	verification_token INTEGER,
	verification_token_sent_at DATETIME,
	PRIMARY KEY (id),
	FOREIGN KEY(role_id) REFERENCES roles (id)
)

;


CREATE TABLE action_logs (
	id INTEGER NOT NULL,
	user_id INTEGER,
	log_type VARCHAR(8),
	action_type VARCHAR(18),
	description TEXT,
	date DATETIME,
	PRIMARY KEY (id),
	FOREIGN KEY(user_id) REFERENCES users (id) ON DELETE SET NULL
)

;


CREATE TABLE profiles (
	id INTEGER NOT NULL,
	user_id INTEGER,
	first_name VARCHAR,
	last_name VARCHAR,
	photo VARCHAR,
	nb_like INTEGER,
	created_at DATETIME,
	updated_at DATETIME,
	PRIMARY KEY (id),
	UNIQUE (user_id),
	FOREIGN KEY(user_id) REFERENCES users (id)
)

;


CREATE TABLE signaled_users (
	id INTEGER NOT NULL,
	user_signaled_id INTEGER,
	reason_id INTEGER,
	created_at DATETIME,
	user_id INTEGER,
	status VARCHAR,
	PRIMARY KEY (id),
	FOREIGN KEY(user_signaled_id) REFERENCES users (id),
	FOREIGN KEY(reason_id) REFERENCES reasons (id),
	FOREIGN KEY(user_id) REFERENCES users (id)
)

;


CREATE TABLE events (
	id INTEGER NOT NULL,
	title VARCHAR,
	description TEXT,
	nb_places INTEGER,
	price DOUBLE,
	profile_id INTEGER,
	nb_likes INTEGER,
	nb_comments INTEGER,
	date DATETIME,
	cloture_billets DATETIME,
	address_id INTEGER,
	created_at DATETIME,
	updated_at DATETIME,
	PRIMARY KEY (id),
	FOREIGN KEY(profile_id) REFERENCES profiles (id),
	FOREIGN KEY(address_id) REFERENCES addresses (id)
)

;


CREATE TABLE comments (
	id INTEGER NOT NULL,
	content VARCHAR,
	profile_id INTEGER,
	event_id INTEGER,
	created_at DATETIME,
	PRIMARY KEY (id),
	FOREIGN KEY(profile_id) REFERENCES profiles (id),
	FOREIGN KEY(event_id) REFERENCES events (id)
)

;


CREATE TABLE event_pictures (
	id INTEGER NOT NULL,
	event_id INTEGER,
	photo VARCHAR,
	uuid UUID,
	PRIMARY KEY (id),
	FOREIGN KEY(event_id) REFERENCES events (id)
)

;


CREATE TABLE event_type (
	event_id INTEGER NOT NULL,
	type_id INTEGER NOT NULL,
	PRIMARY KEY (event_id, type_id),
	FOREIGN KEY(event_id) REFERENCES events (id),
	FOREIGN KEY(type_id) REFERENCES types (id)
)

;


CREATE TABLE likes (
	id INTEGER NOT NULL,
	profile_id INTEGER,
	event_id INTEGER,
	created_at DATETIME,
	PRIMARY KEY (id),
	FOREIGN KEY(profile_id) REFERENCES profiles (id),
	FOREIGN KEY(event_id) REFERENCES events (id)
)

;


CREATE TABLE payments (
	id INTEGER NOT NULL,
	event_id INTEGER NOT NULL,
	event_title VARCHAR NOT NULL,
	buyer_id INTEGER,
	buyer_email VARCHAR NOT NULL,
	organizer_id INTEGER,
	organizer_email VARCHAR NOT NULL,
	amount DOUBLE,
	fee DOUBLE,
	brut_amount DOUBLE,
	stripe_session_id VARCHAR,
	stripe_payment_intent_id VARCHAR,
	status VARCHAR,
	created_at DATETIME,
	PRIMARY KEY (id),
	FOREIGN KEY(event_id) REFERENCES events (id),
	FOREIGN KEY(buyer_id) REFERENCES users (id) ON DELETE SET NULL,
	FOREIGN KEY(organizer_id) REFERENCES users (id)
)

;


CREATE TABLE registrations (
	id INTEGER NOT NULL,
	profile_id INTEGER,
	event_id INTEGER,
	registered_at DATETIME,
	payment_status VARCHAR,
	PRIMARY KEY (id),
	FOREIGN KEY(profile_id) REFERENCES profiles (id),
	FOREIGN KEY(event_id) REFERENCES events (id)
)

;


CREATE TABLE signaled_events (
	id INTEGER NOT NULL,
	event_id INTEGER,
	reason_id INTEGER,
	created_at DATETIME,
	user_id INTEGER,
	status VARCHAR,
	PRIMARY KEY (id),
	FOREIGN KEY(event_id) REFERENCES events (id),
	FOREIGN KEY(reason_id) REFERENCES reasons (id),
	FOREIGN KEY(user_id) REFERENCES users (id)
)

;


CREATE TABLE signaled_comments (
	id INTEGER NOT NULL,
	comment_id INTEGER,
	reason_id INTEGER,
	created_at DATETIME,
	user_id INTEGER,
	status VARCHAR,
	PRIMARY KEY (id),
	FOREIGN KEY(comment_id) REFERENCES comments (id),
	FOREIGN KEY(reason_id) REFERENCES reasons (id),
	FOREIGN KEY(user_id) REFERENCES users (id)
)

;

