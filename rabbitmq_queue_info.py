#!/usr/bin/env python

# ---------------------------------------------------------
# This script calls RabbitMQ REST API to get a queue info.
# Uses request module, which has been tested up to python 3.7.
# 
# input arguments:
#   --endpoint: the RabbitMQ API endpoint. e.g. "https://mozart.mycluster.hysds.io:15673" see http://e-jobs.aria.hysds.io:15672/api/
#   --username: username for rabbitmq
#   --passwd: password for rabbitmq
#   --queue: (optional) name of queue. if specified, it will only return info for this queue name. if not specified, then all queues will be shown.
#
# outputs to stdout:
#   <queue name> <state> <messages_ready> <messages_unacknowledged>
#
# example usage:
#   rabbitmq_queue_info.py --endpoint="https://mozart.mycluster.hysds.io:15673" --username=guest --passwd=guest [--queue=standard_product-s1gunw-topsapp-pleiade]
#   standard_product-s1gunw-topsapp-pleiades running 0 0
#
# ---------------------------------------------------------


import logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.WARNING, format='%(asctime)s %(name)s.%(funcName)s +%(lineno)s: %(levelname)-8s [%(process)d] %(message)s')


def get_queues(url, http_basic_auth_credentials):
    """
    Queries RabbitMQ's REST API to get queue information.
    @return: list of queue dicts
    """

    import requests
    logger.debug( "calling url {} with credentials {}".format(url, http_basic_auth_credentials) )
    # using verify=False just in case some rabbitmq endpoint yields OpenSSL.SSL.Error: [('SSL routines', 'tls_process_server_certificate', 'certificate verify failed')]
    response = requests.get(url, auth=http_basic_auth_credentials, verify=False)

    # exit if error so outter scripts calling this python scripts can detect for non-zero exit code
    if response.status_code != 200:
        logger.error( "got error http {} from {}".format(url, response.status_code) )
        raise Exception( "got error http {} from {}".format(url, response.status_code) )

    logger.debug( "response: {}".format(response) )

    # get json stream of http response
    queues = response.json()
    # returns list of queue dicts

    # [
    #     {
    #         "arguments": {
    #             "x-max-priority": 10
    #         },
    #         "auto_delete": false,
    #         "backing_queue_status": {
    #             "avg_ack_egress_rate": 0.0,
    #             "avg_ack_ingress_rate": 0.0,
    #             "avg_egress_rate": 0.0,
    #             "avg_ingress_rate": 0.0,
    #             "delta": [
    #                 "delta",
    #                 "todo",
    #                 "todo",
    #                 "todo",
    #                 "todo"
    #             ],
    #             "len": 1,
    #             "mode": "default",
    #             "next_seq_id": 1,
    #             "priority_lengths": {
    #                 "0": 0,
    #                 "1": 0,
    #                 "10": 0,
    #                 "2": 0,
    #                 "3": 0,
    #                 "4": 0,
    #                 "5": 1,
    #                 "6": 0,
    #                 "7": 0,
    #                 "8": 0,
    #                 "9": 0
    #             },
    #             "q1": 0,
    #             "q2": 0,
    #             "q3": 0,
    #             "q4": 1,
    #             "target_ram_count": "infinity"
    #         },
    #         "consumer_utilisation": null,
    #         "consumers": 0,
    #         "durable": true,
    #         "exclusive": false,
    #         "exclusive_consumer_tag": null,
    # ...
    #         "consumer_utilisation": null,
    #         "consumers": 4,
    #         "durable": true,
    #         "exclusive": false,
    #         "exclusive_consumer_tag": null,
    #         "garbage_collection": {
    #             "fullsweep_after": 65535,
    #             "min_bin_vheap_size": 46422,
    #             "min_heap_size": 233,
    #             "minor_gcs": 248
    #         },
    #         "head_message_timestamp": null,
    #         "idle_since": "2020-03-23 22:48:25",
    #         "memory": 81416,
    #         "message_bytes": 0,
    #         "message_bytes_paged_out": 0,
    #         "message_bytes_persistent": 0,
    #         "message_bytes_ram": 0,
    #         "message_bytes_ready": 0,
    #         "message_bytes_unacknowledged": 0,
    #         "messages": 0,
    #         "messages_details": {
    #             "rate": 0.0
    #         },
    #         "messages_paged_out": 0,
    #         "messages_persistent": 0,
    #         "messages_ram": 0,
    #         "messages_ready": 0,
    #         "messages_ready_details": {
    #             "rate": 0.0
    #         },
    #         "messages_ready_ram": 0,
    #         "messages_unacknowledged": 0,
    #         "messages_unacknowledged_details": {
    #             "rate": 0.0
    #         },
    #         "messages_unacknowledged_ram": 0,
    #         "name": "user_rules_trigger",
    #         "node": "rabbit@localhost",
    #         "policy": null,
    #         "recoverable_slaves": null,
    #         "reductions": 490785,
    #         "reductions_details": {
    #             "rate": 0.0
    #         },
    #         "state": "running",
    #         "vhost": "/"
    #     }
    # ]

    import json
    logger.debug(json.dumps(queues, indent=4, sort_keys=True))

    return queues


def print_queue(queue):
    """
    Outputs to stdout the given queue's key information.
    Allows outter tools calling this script to parse the queue info.
    @param queue: dict of queue info
    <queue name> <state> <messages_ready> <messages_unacknowledged>
    """

    queue_name = queue["name"]
    logger.debug( "queue_name: {}".format(queue_name) )

    queue_state = queue["state"]
    logger.debug( "queue_state: {}".format(queue_state) )

    messages_ready = queue["messages_ready"]
    logger.debug( "messages_ready: {}".format(messages_ready) )

    messages_unacknowledged = queue["messages_unacknowledged"]
    logger.debug( "messages_unacknowledged: {}".format(messages_unacknowledged) )

    print( "{} {} {} {}".format(queue_name, queue_state, messages_ready, messages_unacknowledged) )



# ---------------------------------------------------------

def show_usage():
    print('Usage:\n')
    print('rabbitmq_queue_info.py --endpoint="https://mozart.mycluster.hysds.io:15673" --username=guest --passwd=guest [--queue=standard_product-s1gunw-topsapp-pleiade] \n' )


import sys, getopt

def main(argv):

    # ---------------------------------------------------------
    # initialize constants

    # rabbitmq REST API endpoint
    api_endpoint = ''
    api_path = '/api/queues/%2F/'

    # rabbitmq credentials
    rabbitmq_username = ''
    rabbitmq_passwd = ''

    queue_name = ''
    # ---------------------------------------------------------

    try:
        opts, args = getopt.getopt(argv,"he:u:p:q:",["endpoint=","username=","passwd=","queue="])
    except getopt.GetoptError:
        show_usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            show_usage()
            sys.exit()
        elif opt in ("-e", "--endpoint"):
            api_endpoint = arg
        elif opt in ("-u", "--username"):
            username = arg
        elif opt in ("-p", "--passwd"):
            passwd = arg
        elif opt in ("-q", "--queue"):
            queue_name = arg

    if not api_endpoint.strip():
        show_usage()
        sys.exit(2)

    # call rabbitmq REST API
    url = "{}{}{}".format(api_endpoint, api_path, queue_name)
    logger.debug( "url: {}".format(url) )

    # use the credentials
    http_basic_auth_credentials = (username, passwd)

    # call rabbitmq api to get queues info
    queues = get_queues(url, http_basic_auth_credentials)

    # for bulk query of all queues, result is list type
    if isinstance(queues, list):
        # loop through each queue info
        for queue in queues:
            # output queues info to stdout to be picked up by callers of this script
            print_queue(queue)
    # else result is single dict queue
    else:
        # output queues info to stdout to be picked up by callers of this script
        print_queue(queues)


if __name__ == "__main__":
    main(sys.argv[1:])
