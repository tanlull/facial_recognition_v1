
drop table image

CREATE TABLE public.image (
	id integer NOT NULL,
	img_path text NOT NULL,
	img_encoding BYTEA  
);

CREATE TABLE public.profile (
	id serial NOT NULL,
	first_name varchar(100) NULL,
	last_name varchar(100) NULL,
	ba varchar(50) NOT NULL,
	service varchar(20) NULL,
	create_date timestamp NULL DEFAULT CURRENT_TIMESTAMP,
	CONSTRAINT profile_pkey PRIMARY KEY (id)
);
