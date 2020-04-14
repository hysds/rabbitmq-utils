#!/usr/bin/env bash

# ---------------------------------------------------------
# This script calls the rabbitmq tool "rabbitmq_connection.py"
# to query the rabbitmq and outputs to STDOUT log file in SDSWatch log format.
# The intent to output to STDOUT is to ease running this script under supervisord.
# ---------------------------------------------------------

# ------------------------------------------------------------------------------
# Automatically determines the full canonical path of where this script is
# located--regardless of what path this script is called from. (if available)
# ${BASH_SOURCE} works in both sourcing and execing the bash script.
# ${0} only works for when execing the bash script. ${0}==bash when sourcing.
BASE_PATH=$(dirname "${BASH_SOURCE}")
# convert potentially relative path to the full canonical path
BASE_PATH=$(cd "${BASE_PATH}"; pwd)
# get the name of the script
BASE_NAME=$(basename "${BASH_SOURCE}")
# ------------------------------------------------------------------------------


# ---------------------------------------------------------
# input settings

# rabbitmq endpoint
RABBITMQ_API_ENDPOINT="https://mozart.mycluster.hysds.io:15673"
RABBITMQ_USERNAME="meee"
RABBITMQ_PASSWD="mypass"

RABBITMQ_API_ENDPOINT="https://100.67.33.56:15673"
RABBITMQ_USERNAME="hysdsops"
RABBITMQ_PASSWD="Y2FkNTllND"

# query interval to rabbitmq, in seconds
INTERVAL=60

# ---------------------------------------------------------

# the tool for rabbitmq query
RABBITMQ_CONNECTION_PY="${BASE_PATH}/rabbitmq_connection.py"

# check if rabbitmq tool file exists
if [ ! -f "${RABBITMQ_CONNECTION_PY}" ]; then
    echo "No file ${RABBITMQ_CONNECTION_PY} found." 1>&2
    exit 1
fi

while true; do
    TIMESTAMP=$(date +%Y-%m-%dT%H:%M:%S%z)

    ${RABBITMQ_CONNECTION_PY} --endpoint="${RABBITMQ_API_ENDPOINT}" --username="${RABBITMQ_USERNAME}" --passwd="${RABBITMQ_PASSWD}" | awk '{print $1"->"$3" "$4" "$6" "$7}' | while read LINE; do
        IFS=" " read NAME STATE CLIENT_SEND_RATE CLIENT_RECV_RATE <<< ${LINE}
        # echo "# NAME: ${NAME}"
        # echo "# STATE: ${STATE}"
        # echo "# CLIENT_SEND_RATE: ${CLIENT_SEND_RATE}"
        # echo "# CLIENT_RECV_RATE: ${CLIENT_RECV_RATE}"
        echo "${TIMESTAMP} , ${RABBITMQ_API_ENDPOINT} , rabbitmq.connection , ${NAME} , state, ${STATE} "
        echo "${TIMESTAMP} , ${RABBITMQ_API_ENDPOINT} , rabbitmq.connection , ${NAME} , client_send_rate, ${CLIENT_SEND_RATE} "
        echo "${TIMESTAMP} , ${RABBITMQ_API_ENDPOINT} , rabbitmq.connection , ${NAME} , client_recv_rate, ${CLIENT_RECV_RATE} "
    done

    sleep ${INTERVAL}
done

