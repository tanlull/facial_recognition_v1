CREATE TABLE public.image (
	id varchar(50) NOT NULL,
	img_path text NOT NULL,
	img_encoding BYTEA  
);

CREATE TABLE public.profile (
	id serial NOT NULL,
	first_name bpchar(100) NULL,
	last_name bpchar(100) NULL,
	ba bpchar(50) NOT NULL,
	service bpchar(20) NULL,
	create_date timestamp NULL DEFAULT CURRENT_TIMESTAMP,
	CONSTRAINT profile_pkey PRIMARY KEY (id)
);
