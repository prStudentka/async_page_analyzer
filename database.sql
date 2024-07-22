CREATE TABLE IF NOT EXISTS urls (
	id bigint PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    name VARCHAR(255),
	created_at DATE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS url_checks (
    id bigint PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
	url_id integer,
	status_code integer,
	h1 varchar(255),
	title varchar(60),
	description varchar(255),
	created_at Date DEFAULT CURRENT_TIMESTAMP
);
