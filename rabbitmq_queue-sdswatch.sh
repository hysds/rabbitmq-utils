#!/usr/bin/env bash

# ---------------------------------------------------------
# This script calls the rabbitmq tool "rabbitmq_queue.py"
# to query the job queues (ignoring celery queues) and outputs
# to STDOUT log file in SDSWatch log format. The intent to output
# to STDOUT is to ease running this script under supervisord.
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

# query interval to rabbitmq, in seconds
INTERVAL=60

# ---------------------------------------------------------

# the tool for rabbitmq query
RABBITMQ_QUEUE_PY="${BASE_PATH}/rabbitmq_queue.py"

# check if rabbitmq tool file exists
if [ ! -f "${RABBITMQ_QUEUE_PY}" ]; then
    echo "No file ${RABBITMQ_QUEUE_PY} found." 1>&2
    exit 1
fi

while true; do
    TIMESTAMP=$(date +%Y-%m-%dT%H:%M:%S%z)

    ${RABBITMQ_QUEUE_PY} --endpoint="${RABBITMQ_API_ENDPOINT}" --username="${RABBITMQ_USERNAME}" --passwd="${RABBITMQ_PASSWD}" | grep -v celery | while read LINE; do
        IFS=" " read RABBITMQ_QUEUE RABBITMQ_STATE RABBITMQ_READY RABBITMQ_UNACKED <<< ${LINE}
        # echo "# RABBITMQ_QUEUE: ${RABBITMQ_QUEUE}"
        # echo "# RABBITMQ_STATE: ${RABBITMQ_STATE}"
        # echo "# RABBITMQ_READY: ${RABBITMQ_READY}"
        # echo "# RABBITMQ_UNACKED: ${RABBITMQ_UNACKED}"
        echo "${TIMESTAMP} , ${RABBITMQ_API_ENDPOINT} , rabbitmq.queue , ${RABBITMQ_QUEUE} , state, ${RABBITMQ_STATE} "
        echo "${TIMESTAMP} , ${RABBITMQ_API_ENDPOINT} , rabbitmq.queue , ${RABBITMQ_QUEUE} , ready, ${RABBITMQ_READY} "
        echo "${TIMESTAMP} , ${RABBITMQ_API_ENDPOINT} , rabbitmq.queue , ${RABBITMQ_QUEUE} , unacked, ${RABBITMQ_UNACKED} "
    done

    sleep ${INTERVAL}
done

