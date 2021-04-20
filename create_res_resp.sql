-- Table: public.sfs_resp

-- DROP TABLE public.sfs_resp;

CREATE TABLE public.sfs_resp
(
    resp_id numeric NOT NULL,
    resp_survey_id numeric NOT NULL,
    resp_q_id numeric NOT NULL,
    resp_points numeric,
    resp_comment boolean,
    resp_form_key character varying COLLATE pg_catalog."default" NOT NULL,
	
	CONSTRAINT sfs_resppk PRIMARY KEY (resp_id),
	CONSTRAINT sfs_respfk_resp_survey_id FOREIGN KEY (resp_survey_id)
        REFERENCES public.sfs_surv (sur_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE RESTRICT
        NOT VALID
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.sfs_resp
    OWNER to postgres;
	
	
	