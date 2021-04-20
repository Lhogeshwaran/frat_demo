-- Table: public.sfs_surv

-- DROP TABLE public.sfs_surv;

CREATE TABLE public.sfs_surv
(
    sur_id numeric NOT NULL,
    sur_year numeric NOT NULL,
    sur_subject_code character varying COLLATE pg_catalog."default" NOT NULL,
    sur_subject_id numeric NOT NULL,
    sur_subject_name character varying COLLATE pg_catalog."default" NOT NULL,
    sur_faculty_id character varying COLLATE pg_catalog."default" NOT NULL,
    sur_faculty_name character varying COLLATE pg_catalog."default" NOT NULL,
    sur_acadunit_id character varying COLLATE pg_catalog."default" NOT NULL,
    sur_acadunit_name character varying COLLATE pg_catalog."default" NOT NULL,
    sur_student_count numeric NOT NULL,
	
	CONSTRAINT sfs_survpk PRIMARY KEY (sur_id),
	CONSTRAINT public_sfs_surv_sur_year CHECK (sur_year = ANY (ARRAY[2014::numeric, 2015::numeric, 2016::numeric, 2017::numeric, 2018::numeric, 2019::numeric]))
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.sfs_surv
    OWNER to postgres;