#!/bin/bash
POSITIONAL=()
while [[ $# -gt 0 ]]; do
key="$1"
case $key in
    -h|--db-host)
    DB_HOST="$2"
    shift # past argument
    shift # past value
    ;;
    -du|--default-db-user)
    DEFAULT_DB_USER="$2"
    shift # past argument
    shift # past value
    ;;
    -dp|--default-db-password)
    DB_PASSWORD="$2"
    shift # past argument
    shift # past value
    ;;
    -idm|--idm-db)
    IDM_DB="$2"
    shift # past argument
    shift # past value
    ;;
    -idmu|--idm-db-user)
    IDM_DB_USER="$2"
    shift # past argument
    shift # past value
    ;;
    -idmp|--idm-db-password)
    IDM_DB_PASSWORD="$2"
    shift # past argument
    shift # past value
    ;;
    -cdf|--cdf-api-db)
    CDF_API_DB="$2"
    shift # past argument
    shift # past value
    ;;
    -cdfu|--cdf-api-db-user)
    CDF_API_DB_USER="$2"
    shift # past argument
    shift # past value
    ;;
    -cdfp|--cdf-api-db-password)
    CDF_API_DB_PASSWORD="$2"
    shift # past argument
    shift # past value
    ;;
    *) # unknown option
    POSITIONAL+=("$1") # save it in an array for later
    shift # past argument
    ;;
esac
done
set -- "${POSITIONAL[@]}" # restore positional parameters

if [ -z "$IDM_DB" ]
then
    IDM_DB="cdfidm"
fi

if [ -z "$IDM_DB_USER" ]
then
    IDM_DB_USER="cdfidmuser"
fi

if [ -z "$CDF_API_DB" ]
then
    CDF_API_DB="cdfapiserverdb"
fi

if [ -z "$CDF_API_DB_USER" ]
then
    CDF_API_DB_USER="cdfapiserver"
fi

psql "sslmode=disable dbname=postgres \
    user=$DEFAULT_DB_USER \
    password=$DB_PASSWORD \
    hostaddr=$DB_HOST" << EOF
ALTER USER postgres WITH PASSWORD '$DB_PASSWORD';
EOF

psql "sslmode=disable dbname=postgres \
    user=postgres \
    password=$DB_PASSWORD \
    hostaddr=$DB_HOST" << EOF
GRANT ALL PRIVILEGES ON DATABASE postgres to postgres;
CREATE SCHEMA postgres AUTHORIZATION postgres;
DROP DATABASE IF EXISTS $CDF_CDF_API_DB
DROP ROLE IF EXISTS $CDF_API_DB_USER
DROP DATABASE IF EXISTS $IDM_DB
DROP ROLE IF EXISTS $IDM_DB_USER
EOF

psql "sslmode=disable dbname=postgres \
    user=postgres \
    password=$DB_PASSWORD \
    hostaddr=$DB_HOST" << EOF
CREATE USER $IDM_DB_USER Login PASSWORD '$IDM_DB_PASSWORD';
GRANT $IDM_DB_USER TO postgres;
CREATE DATABASE $IDM_DB WITH owner=$IDM_DB_USER;
EOF

psql "sslmode=disable dbname=$IDM_DB \
    user=postgres \
    password=$DB_PASSWORD \
    hostaddr=$DB_HOST" << EOF
ALTER SCHEMA public OWNER TO $IDM_DB_USER;
ALTER SCHEMA public RENAME TO $IDM_DB_USER;
REVOKE ALL ON SCHEMA $IDM_DB_USER from public;
GRANT ALL ON SCHEMA $IDM_DB_USER to $IDM_DB_USER;
ALTER USER $IDM_DB_USER SET search_path TO $IDM_DB_USER;
EOF

psql "sslmode=disable dbname=postgres \
    user=postgres \
    password=$DB_PASSWORD \
    hostaddr=$DB_HOST" << EOF
CREATE USER $CDF_API_DB_USER login PASSWORD '$CDF_API_DB_PASSWORD';
GRANT $CDF_API_DB_USER  TO postgres;
CREATE DATABASE $CDF_API_DB WITH OWNER=$CDF_API_DB_USER;
EOF

psql "sslmode=disable dbname=$CDF_API_DB \
    user=postgres \
    password=$DB_PASSWORD \
    hostaddr=$DB_HOST" << EOF
ALTER SCHEMA public OWNER TO $CDF_API_DB_USER;
ALTER SCHEMA public RENAME TO $CDF_API_DB_USER;
REVOKE ALL ON SCHEMA $CDF_API_DB_USER FROM public;
GRANT ALL ON SCHEMA $CDF_API_DB_USER TO $CDF_API_DB_USER;
ALTER USER $CDF_API_DB_USER SET search_path TO $CDF_API_DB_USER;
EOF