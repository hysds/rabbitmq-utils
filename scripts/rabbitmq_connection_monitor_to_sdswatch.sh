#!/usr/bin/env bash

# ---------------------------------------------------------
# This script calls the rabbitmq tool "rabbitmq_connection_monitor.py"
# to query the rabbitmq connection and outputs to STDOUT log file in SDSWatch log format.
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

# add this package's build to this scripts PYTHONPATH to make it work without install.
BUILD_LIB=$(cd "${BASE_PATH}/../build/lib/"; pwd)
export PYTHONPATH="${PYTHONPATH}:${BUILD_LIB}"

# ---------------------------------------------------------
# input settings

# rabbitmq endpoint
RABBITMQ_API_ENDPOINT="https://mozart.mycluster.hysds.io:15673"
RABBITMQ_USERNAME="meee"
RABBITMQ_PASSWD="mypass"

RABBITMQ_API_ENDPOINT="https://100.67.33.56:15673"
RABBITMQ_USERNAME="hysdsops"
RABBITMQ_PASSWD="Y2FkNTllND"

# how often to check rabbitmq endpoint, in unit seconds
INTERVAL=60

# ---------------------------------------------------------

# the tool for rabbitmq query
RABBITMQ_CONNECTION_PY="${BASE_PATH}/rabbitmq_connection_monitor.py"

# check if rabbitmq tool file exists
if [ ! -f "${RABBITMQ_CONNECTION_PY}" ]; then
    echo "No file ${RABBITMQ_CONNECTION_PY} found." 1>&2
    exit 1
fi

# convert output streamed to sdswatch format
${RABBITMQ_CONNECTION_PY} --endpoint="${RABBITMQ_API_ENDPOINT}" --username="${RABBITMQ_USERNAME}" --passwd="${RABBITMQ_PASSWD}" --interval="${INTERVAL}" 2> ${BASE_NAME}.stderr | while IFS= read -r LINE; do
    # timestamp, connection_name, connection_state, connection_send_rate, connection_recv_rate
    IFS=" " read TIMESTAMP CLIENT ARROW SERVER STATE CONN_SEND_RATE CONN_RECV_RATE <<< ${LINE}
    NAME="${CLIENT}->${SERVER}"
    echo "${TIMESTAMP} , ${RABBITMQ_API_ENDPOINT} , rabbitmq.connection , ${NAME} , state, ${STATE} "
    echo "${TIMESTAMP} , ${RABBITMQ_API_ENDPOINT} , rabbitmq.connection , ${NAME} , send_rate_to_client, ${CONN_SEND_RATE} "
    echo "${TIMESTAMP} , ${RABBITMQ_API_ENDPOINT} , rabbitmq.connection , ${NAME} , recv_rate_from_client, ${CONN_RECV_RATE} "
done

