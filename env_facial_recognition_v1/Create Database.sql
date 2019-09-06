use face;


CREATE TABLE public.profile (
	id serial NOT NULL,
	first_name bpchar(100) NULL,
	last_name bpchar(100) NULL,
	ba bpchar(50) NOT NULL,
	service bpchar(20) NULL,
	create_date timestamp NULL DEFAULT CURRENT_TIMESTAMP,
	CONSTRAINT profile_pkey PRIMARY KEY (id)
);



CREATE TABLE image (
    id INTEGER NOT NULL,
    img_path TEXT  NOT NULL,
    img_encoding TEXT 
);

