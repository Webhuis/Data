--
-- PostgreSQL database dump
--

-- Dumped from database version 11.20 (Debian 11.20-0+deb10u1)
-- Dumped by pg_dump version 14.9 (Ubuntu 14.9-0ubuntu0.22.04.1)

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

--
-- Name: context; Type: SCHEMA; Schema: -; Owner: www_data
--

CREATE SCHEMA context;


ALTER SCHEMA context OWNER TO www_data;

--
-- Name: feeds; Type: SCHEMA; Schema: -; Owner: www_data
--

CREATE SCHEMA feeds;


ALTER SCHEMA feeds OWNER TO www_data;

--
-- Name: knowledge; Type: SCHEMA; Schema: -; Owner: www_data
--

CREATE SCHEMA knowledge;


ALTER SCHEMA knowledge OWNER TO www_data;

SET default_tablespace = '';

--
-- Name: domain; Type: TABLE; Schema: context; Owner: www_data
--

CREATE TABLE context.domain (
    id bigint NOT NULL,
    domain_name character varying NOT NULL,
    domain_data jsonb
);


ALTER TABLE context.domain OWNER TO www_data;

--
-- Name: domain_id_seq; Type: SEQUENCE; Schema: context; Owner: www_data
--

ALTER TABLE context.domain ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME context.domain_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: domain_role; Type: TABLE; Schema: context; Owner: www_data
--

CREATE TABLE context.domain_role (
    id bigint NOT NULL,
    domain_name character varying NOT NULL,
    role_code character varying NOT NULL,
    domain_role_data jsonb
);


ALTER TABLE context.domain_role OWNER TO www_data;

--
-- Name: domain_role_id_seq; Type: SEQUENCE; Schema: context; Owner: www_data
--

ALTER TABLE context.domain_role ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME context.domain_role_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: fqhost; Type: TABLE; Schema: context; Owner: www_data
--

CREATE TABLE context.fqhost (
    id bigint NOT NULL,
    uqhost character varying NOT NULL,
    domain_name character varying NOT NULL,
    role_code character(4) NOT NULL,
    "timestamp" timestamp with time zone,
    last_seen timestamp with time zone
);


ALTER TABLE context.fqhost OWNER TO www_data;

--
-- Name: role_service; Type: TABLE; Schema: context; Owner: www_data
--

CREATE TABLE context.role_service (
    id bigint NOT NULL,
    role_code character varying NOT NULL,
    service_type character varying NOT NULL
);


ALTER TABLE context.role_service OWNER TO www_data;

--
-- Name: service; Type: TABLE; Schema: context; Owner: www_data
--

CREATE TABLE context.service (
    id bigint NOT NULL,
    service_type character varying NOT NULL,
    service_port smallint NOT NULL,
    service_name character varying NOT NULL,
    check_line character varying,
    interface character varying NOT NULL
);


ALTER TABLE context.service OWNER TO www_data;

--
-- Name: fqhost_services; Type: VIEW; Schema: context; Owner: www_data
--

CREATE VIEW context.fqhost_services AS
 SELECT fq.uqhost,
    fq.domain_name,
    rs.service_type,
    sv.interface,
    sv.service_port
   FROM ((context.fqhost fq
     JOIN context.role_service rs ON ((fq.role_code = (rs.role_code)::bpchar)))
     JOIN context.service sv ON (((rs.service_type)::text = (sv.service_type)::text)));


ALTER TABLE context.fqhost_services OWNER TO www_data;

--
-- Name: host_id_seq; Type: SEQUENCE; Schema: context; Owner: www_data
--

ALTER TABLE context.fqhost ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME context.host_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: role; Type: TABLE; Schema: context; Owner: www_data
--

CREATE TABLE context.role (
    id bigint NOT NULL,
    role_code character(4) NOT NULL,
    role_name character varying
);


ALTER TABLE context.role OWNER TO www_data;

--
-- Name: role_id_seq; Type: SEQUENCE; Schema: context; Owner: www_data
--

ALTER TABLE context.role ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME context.role_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: role_service_id_seq; Type: SEQUENCE; Schema: context; Owner: www_data
--

ALTER TABLE context.role_service ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME context.role_service_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: service_id_seq; Type: SEQUENCE; Schema: context; Owner: www_data
--

ALTER TABLE context.service ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME context.service_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: hard_classes; Type: TABLE; Schema: feeds; Owner: www_data
--

CREATE TABLE feeds.hard_classes (
    id bigint NOT NULL,
    uqhost character varying NOT NULL,
    domain character varying NOT NULL,
    os character varying,
    ostype character varying,
    flavor character varying,
    cpus smallint,
    arch character varying,
    "timestamp" timestamp with time zone
);


ALTER TABLE feeds.hard_classes OWNER TO www_data;

--
-- Name: TABLE hard_classes; Type: COMMENT; Schema: feeds; Owner: www_data
--

COMMENT ON TABLE feeds.hard_classes IS 'CFEngine Hard Classes';


--
-- Name: hard_classes_id_seq; Type: SEQUENCE; Schema: feeds; Owner: www_data
--

ALTER TABLE feeds.hard_classes ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME feeds.hard_classes_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: host_objects; Type: TABLE; Schema: feeds; Owner: www_data
--

CREATE TABLE feeds.host_objects (
    id bigint NOT NULL,
    uqhost character varying NOT NULL,
    domain character varying NOT NULL,
    object_id text NOT NULL
);


ALTER TABLE feeds.host_objects OWNER TO www_data;

--
-- Name: TABLE host_objects; Type: COMMENT; Schema: feeds; Owner: www_data
--

COMMENT ON TABLE feeds.host_objects IS 'CFEngine Host Objects in process';


--
-- Name: host_objects_id_seq; Type: SEQUENCE; Schema: feeds; Owner: www_data
--

ALTER TABLE feeds.host_objects ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME feeds.host_objects_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: json_in; Type: TABLE; Schema: feeds; Owner: www_data
--

CREATE TABLE feeds.json_in (
    id bigint NOT NULL,
    message_time timestamp with time zone NOT NULL,
    message_in jsonb,
    message_flow smallint DEFAULT 0
);


ALTER TABLE feeds.json_in OWNER TO www_data;

--
-- Name: TABLE json_in; Type: COMMENT; Schema: feeds; Owner: www_data
--

COMMENT ON TABLE feeds.json_in IS 'CFEngine ZMQ messages';


--
-- Name: json_in_id_seq; Type: SEQUENCE; Schema: feeds; Owner: www_data
--

ALTER TABLE feeds.json_in ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME feeds.json_in_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: response; Type: TABLE; Schema: feeds; Owner: www_data
--

CREATE TABLE feeds.response (
    id bigint NOT NULL,
    feed_message_time timestamp with time zone NOT NULL,
    response_time timestamp with time zone NOT NULL,
    message_out jsonb
);


ALTER TABLE feeds.response OWNER TO www_data;

--
-- Name: response_id_seq; Type: SEQUENCE; Schema: feeds; Owner: www_data
--

ALTER TABLE feeds.response ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME feeds.response_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: domain p_domain; Type: CONSTRAINT; Schema: context; Owner: www_data
--

ALTER TABLE ONLY context.domain
    ADD CONSTRAINT p_domain PRIMARY KEY (domain_name);


--
-- Name: domain_role p_domain_role; Type: CONSTRAINT; Schema: context; Owner: www_data
--

ALTER TABLE ONLY context.domain_role
    ADD CONSTRAINT p_domain_role PRIMARY KEY (domain_name, role_code);


--
-- Name: fqhost p_host; Type: CONSTRAINT; Schema: context; Owner: www_data
--

ALTER TABLE ONLY context.fqhost
    ADD CONSTRAINT p_host PRIMARY KEY (uqhost, domain_name);


--
-- Name: role p_role; Type: CONSTRAINT; Schema: context; Owner: www_data
--

ALTER TABLE ONLY context.role
    ADD CONSTRAINT p_role PRIMARY KEY (role_code);


--
-- Name: role_service p_role_service; Type: CONSTRAINT; Schema: context; Owner: www_data
--

ALTER TABLE ONLY context.role_service
    ADD CONSTRAINT p_role_service PRIMARY KEY (role_code, service_type);


--
-- Name: service p_service_type; Type: CONSTRAINT; Schema: context; Owner: www_data
--

ALTER TABLE ONLY context.service
    ADD CONSTRAINT p_service_type PRIMARY KEY (service_type);


--
-- Name: hard_classes p_hard_classes; Type: CONSTRAINT; Schema: feeds; Owner: www_data
--

ALTER TABLE ONLY feeds.hard_classes
    ADD CONSTRAINT p_hard_classes PRIMARY KEY (uqhost, domain);


--
-- Name: host_objects p_host_objects; Type: CONSTRAINT; Schema: feeds; Owner: www_data
--

ALTER TABLE ONLY feeds.host_objects
    ADD CONSTRAINT p_host_objects PRIMARY KEY (uqhost, domain);


--
-- Name: json_in p_json_in; Type: CONSTRAINT; Schema: feeds; Owner: www_data
--

ALTER TABLE ONLY feeds.json_in
    ADD CONSTRAINT p_json_in PRIMARY KEY (message_time);


--
-- Name: i_hard_classes; Type: INDEX; Schema: feeds; Owner: www_data
--

CREATE INDEX i_hard_classes ON feeds.hard_classes USING btree (id);


--
-- Name: fqhost f_domain; Type: FK CONSTRAINT; Schema: context; Owner: www_data
--

ALTER TABLE ONLY context.fqhost
    ADD CONSTRAINT f_domain FOREIGN KEY (domain_name) REFERENCES context.domain(domain_name);


--
-- Name: domain_role f_domain_role_domain; Type: FK CONSTRAINT; Schema: context; Owner: www_data
--

ALTER TABLE ONLY context.domain_role
    ADD CONSTRAINT f_domain_role_domain FOREIGN KEY (domain_name) REFERENCES context.domain(domain_name);


--
-- Name: domain_role f_domain_role_role; Type: FK CONSTRAINT; Schema: context; Owner: www_data
--

ALTER TABLE ONLY context.domain_role
    ADD CONSTRAINT f_domain_role_role FOREIGN KEY (role_code) REFERENCES context.role(role_code);


--
-- Name: fqhost f_role; Type: FK CONSTRAINT; Schema: context; Owner: www_data
--

ALTER TABLE ONLY context.fqhost
    ADD CONSTRAINT f_role FOREIGN KEY (role_code) REFERENCES context.role(role_code);


--
-- Name: role_service f_role_role; Type: FK CONSTRAINT; Schema: context; Owner: www_data
--

ALTER TABLE ONLY context.role_service
    ADD CONSTRAINT f_role_role FOREIGN KEY (role_code) REFERENCES context.role(role_code);


--
-- Name: role_service f_service_serviice_type; Type: FK CONSTRAINT; Schema: context; Owner: www_data
--

ALTER TABLE ONLY context.role_service
    ADD CONSTRAINT f_service_serviice_type FOREIGN KEY (service_type) REFERENCES context.service(service_type);


--
-- Name: host_objects f_fqdn; Type: FK CONSTRAINT; Schema: feeds; Owner: www_data
--

ALTER TABLE ONLY feeds.host_objects
    ADD CONSTRAINT f_fqdn FOREIGN KEY (uqhost, domain) REFERENCES feeds.hard_classes(uqhost, domain);


--
-- Name: response f_json_in; Type: FK CONSTRAINT; Schema: feeds; Owner: www_data
--

ALTER TABLE ONLY feeds.response
    ADD CONSTRAINT f_json_in FOREIGN KEY (feed_message_time) REFERENCES feeds.json_in(message_time);


--
-- PostgreSQL database dump complete
--

