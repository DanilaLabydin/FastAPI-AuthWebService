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
-- Name: token; Type: TABLE; Schema: public; Owner: fastapi_auth_user
--

CREATE TABLE public.token (
    id integer NOT NULL,
    token character varying,
    expires timestamp without time zone,
    user_id integer
);


ALTER TABLE public.token OWNER TO fastapi_auth_user;

--
-- Name: token_id_seq; Type: SEQUENCE; Schema: public; Owner: fastapi_auth_user
--

CREATE SEQUENCE public.token_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.token_id_seq OWNER TO fastapi_auth_user;

--
-- Name: token_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: fastapi_auth_user
--

ALTER SEQUENCE public.token_id_seq OWNED BY public.token.id;


--
-- Name: user; Type: TABLE; Schema: public; Owner: fastapi_auth_user
--

CREATE TABLE public."user" (
    id integer NOT NULL,
    username character varying,
    hashed_password character varying,
    salary integer,
    promotion_date timestamp without time zone,
    is_active boolean
);


ALTER TABLE public."user" OWNER TO fastapi_auth_user;

--
-- Name: user_id_seq; Type: SEQUENCE; Schema: public; Owner: fastapi_auth_user
--

CREATE SEQUENCE public.user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.user_id_seq OWNER TO fastapi_auth_user;

--
-- Name: user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: fastapi_auth_user
--

ALTER SEQUENCE public.user_id_seq OWNED BY public."user".id;


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
-- Name: token id; Type: DEFAULT; Schema: public; Owner: fastapi_auth_user
--

ALTER TABLE ONLY public.token ALTER COLUMN id SET DEFAULT nextval('public.token_id_seq'::regclass);


--
-- Name: user id; Type: DEFAULT; Schema: public; Owner: fastapi_auth_user
--

ALTER TABLE ONLY public."user" ALTER COLUMN id SET DEFAULT nextval('public.user_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: fastapi_auth_user
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Name: token token_pkey; Type: CONSTRAINT; Schema: public; Owner: fastapi_auth_user
--

ALTER TABLE ONLY public.token
    ADD CONSTRAINT token_pkey PRIMARY KEY (id);


--
-- Name: token token_token_key; Type: CONSTRAINT; Schema: public; Owner: fastapi_auth_user
--

ALTER TABLE ONLY public.token
    ADD CONSTRAINT token_token_key UNIQUE (token);


--
-- Name: user user_pkey; Type: CONSTRAINT; Schema: public; Owner: fastapi_auth_user
--

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT user_pkey PRIMARY KEY (id);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: fastapi_auth_user
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: ix_token_id; Type: INDEX; Schema: public; Owner: fastapi_auth_user
--

CREATE INDEX ix_token_id ON public.token USING btree (id);


--
-- Name: ix_user_hashed_password; Type: INDEX; Schema: public; Owner: fastapi_auth_user
--

CREATE UNIQUE INDEX ix_user_hashed_password ON public."user" USING btree (hashed_password);


--
-- Name: ix_user_id; Type: INDEX; Schema: public; Owner: fastapi_auth_user
--

CREATE INDEX ix_user_id ON public."user" USING btree (id);


--
-- Name: ix_user_username; Type: INDEX; Schema: public; Owner: fastapi_auth_user
--

CREATE UNIQUE INDEX ix_user_username ON public."user" USING btree (username);


--
-- Name: ix_users_hashed_password; Type: INDEX; Schema: public; Owner: fastapi_auth_user
--

CREATE UNIQUE INDEX ix_users_hashed_password ON public.users USING btree (hashed_password);


--
-- Name: ix_users_id; Type: INDEX; Schema: public; Owner: fastapi_auth_user
--

CREATE INDEX ix_users_id ON public.users USING btree (id);


--
-- Name: ix_users_username; Type: INDEX; Schema: public; Owner: fastapi_auth_user
--

CREATE UNIQUE INDEX ix_users_username ON public.users USING btree (username);


--
-- Name: token token_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: fastapi_auth_user
--

ALTER TABLE ONLY public.token
    ADD CONSTRAINT token_user_id_fkey FOREIGN KEY (user_id) REFERENCES public."user"(id);


--
-- PostgreSQL database dump complete
--

