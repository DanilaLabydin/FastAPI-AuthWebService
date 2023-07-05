--
-- PostgreSQL database dump
--

-- Dumped from database version 15.2 (Ubuntu 15.2-1.pgdg22.04+1)
-- Dumped by pg_dump version 15.2 (Ubuntu 15.2-1.pgdg22.04+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: users; Type: TABLE; Schema: public; Owner: fastapi_auth_user
--

CREATE TABLE public.users (
    id integer NOT NULL,
    username character varying,
    hashed_password character varying,
    salary integer,
    promotion_date timestamp without time zone,
    is_active boolean
);


ALTER TABLE public.users OWNER TO fastapi_auth_user;

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: fastapi_auth_user
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users_id_seq OWNER TO fastapi_auth_user;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: fastapi_auth_user
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: fastapi_auth_user
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: fastapi_auth_user
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: ix_users_hashed_password; Type: INDEX; Schema: public; Owner: fastapi_auth_user
--

CREATE INDEX ix_users_hashed_password ON public.users USING btree (hashed_password);


--
-- Name: ix_users_id; Type: INDEX; Schema: public; Owner: fastapi_auth_user
--

CREATE INDEX ix_users_id ON public.users USING btree (id);


--
-- Name: ix_users_username; Type: INDEX; Schema: public; Owner: fastapi_auth_user
--

CREATE UNIQUE INDEX ix_users_username ON public.users USING btree (username);


--
-- PostgreSQL database dump complete
--

