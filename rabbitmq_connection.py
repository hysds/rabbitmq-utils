#!/usr/bin/env python

# ---------------------------------------------------------
# This script calls RabbitMQ REST API to get a connection info.
# Uses request module, which has been tested up to python 3.7.
# 
# input arguments:
#   --endpoint: the RabbitMQ API endpoint. e.g. "https://mozart.mycluster.hysds.io:15673" see http://e-jobs.aria.hysds.io:15672/api/
#   --username: username for rabbitmq
#   --passwd: password for rabbitmq
#   --connection: (optional) name of connection. if specified, it will only return info for this queue name. if not specified, then all connections will be shown.
#                 format of this string is "127.0.0.1:46542 -> 127.0.0.1:5672"
#
# outputs to stdout:
#   client_host:client_port -> server_host:server_port connection_state channels client_send_rate client_receive_rate
# note that the send/receive rates are in B/s units.
#
# example usage:
# rabbitmq_connection.py --endpoint="https://mozart.mycluster.hysds.io:15673" --username=guest --passwd=guest [--connection="127.0.0.1:46542 -> 127.0.0.1:5672"]
# 123.123.123.123:53836 -> 100.100.100.100:5672 running 2 45.6 0.0
# 123.123.123.123:53838 -> 100.100.100.100:5672 running 1 0.0 0.0
# 123.123.123.123:53840 -> 100.100.100.100:5672 running 1 0.0 0.0
# 123.123.123.123:53842 -> 100.100.100.100:5672 running 1 0.0 0.0
# 123.123.123.123:53844 -> 100.100.100.100:5672 running 2 45.6 0.0
# 123.123.123.123:53846 -> 100.100.100.100:5672 running 2 45.6 0.0
# 123.123.123.123:53848 -> 100.100.100.100:5672 running 1 0.0 0.0
# 123.123.123.123:53850 -> 100.100.100.100:5672 running 1 0.0 0.0
# 123.123.123.123:53852 -> 100.100.100.100:5672 running 1 0.0 0.0
# 123.123.123.123:53854 -> 100.100.100.100:5672 running 1 0.0 0.0
# 123.123.123.123:53856 -> 100.100.100.100:5672 running 1 0.0 0.0
# 127.0.0.1:46162 -> 127.0.0.1:5672 running 1 0.0 0.0
# 127.0.0.1:46170 -> 127.0.0.1:5672 running 1 0.0 0.0
# 127.0.0.1:46222 -> 127.0.0.1:5672 running 2 45.6 0.0
# 127.0.0.1:46226 -> 127.0.0.1:5672 running 2 45.6 0.0
# 127.0.0.1:46230 -> 127.0.0.1:5672 running 2 45.6 0.0
# 127.0.0.1:46232 -> 127.0.0.1:5672 running 2 45.6 0.0
#
# ---------------------------------------------------------


import logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.WARNING, format='%(asctime)s %(name)s.%(funcName)s +%(lineno)s: %(levelname)-8s [%(process)d] %(message)s')


def get_rabbitmq_response(url, http_basic_auth_credentials):
    """
    Queries RabbitMQ's REST API to get JSON response.
    @return: list of dicts
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
    rabbitmq_response = response.json()
    # returns list of dicts

    import json
    logger.debug(json.dumps(rabbitmq_response, indent=4, sort_keys=True))

    return rabbitmq_response


def print_connection(connection):
    """
    Outputs to stdout the given connection's key information.
    Allows outter tools calling this script to parse the connection info.
    @param connection: dict of connection info
    <queue name> <state> <messages_ready> <messages_unacknowledged>
    """

# ]
#     {
#         "auth_mechanism": "AMQPLAIN",
#         "channel_max": 2047,
#         "channels": 1,
#         "client_properties": {
#             "capabilities": {
#                 "authentication_failure_close": true,
#                 "connection.blocked": true,
#                 "consumer_cancel_notify": true
#             },
#             "product": "py-amqp",
#             "product_version": "2.5.2"
#         },
#         "connected_at": 1586466077382,
#         "frame_max": 131072,
#         "garbage_collection": {
#             "fullsweep_after": 65535,
#             "max_heap_size": 0,
#             "min_bin_vheap_size": 46422,
#             "min_heap_size": 233,
#             "minor_gcs": 343
#         },
#         "host": "127.0.0.1",
#         "name": "127.0.0.1:46542 -> 127.0.0.1:5672",
#         "node": "rabbit@localhost",
#         "peer_cert_issuer": null,
#         "peer_cert_subject": null,
#         "peer_cert_validity": null,
#         "peer_host": "127.0.0.1",
#         "peer_port": 46542,
#         "port": 5672,
#         "protocol": "AMQP 0-9-1",
#         "recv_cnt": 7196,
#         "recv_oct": 3069365,
#         "recv_oct_details": {
#             "rate": 0.0
#         },
#         "reductions": 78732471,
#         "reductions_details": {
#             "rate": 180.4
#         },
#         "send_cnt": 7196,
#         "send_oct": 151570,
#         "send_oct_details": {
#             "rate": 0.0
#         },
#         "send_pend": 0,
#         "ssl": false,
#         "ssl_cipher": null,
#         "ssl_hash": null,
#         "ssl_key_exchange": null,
#         "ssl_protocol": null,
#         "state": "running",
#         "timeout": 0,
#         "type": "network",
#         "user": "hysdsops",
#         "user_who_performed_action": "hysdsops",
#         "vhost": "/"
#     }
# ]

    connection_name = connection["name"]
    logger.debug( "connection_name: {}".format(connection_name) )

    connection_state = connection["state"]
    logger.debug( "connection_state: {}".format(connection_state) )

    connection_channels = connection["channels"]
    logger.debug( "connection_channels: {}".format(connection_channels) )

    connection_send_oct_details = connection["send_oct_details"]
    connection_send_rate = connection_send_oct_details["rate"]
    logger.debug( "connection_send_rate: {}".format(connection_send_rate) )

    connection_recv_oct_details = connection["recv_oct_details"]
    connection_recv_rate = connection_recv_oct_details["rate"]
    logger.debug( "connection_recv_rate: {}".format(connection_recv_rate) )

    print( "{} {} {} {} {}".format(connection_name, connection_state, connection_channels, connection_send_rate, connection_recv_rate) )



# ---------------------------------------------------------

def show_usage():
    print('Usage:\n')
    print('rabbitmq_connection.py --endpoint="https://mozart.mycluster.hysds.io:15673" --username=guest --passwd=guest [--connection=ip:port] \n' )


import sys, getopt

def main(argv):

    # ---------------------------------------------------------
    # initialize constants

    # rabbitmq REST API endpoint
    # Many URIs require the name of a virtual host as part of the path, since names only uniquely identify objects within a virtual host. As the default virtual host is called "/", this will need to be encoded as "%2f".
    api_endpoint = ''
    api_path = '/api/connections/'

    # rabbitmq credentials
    rabbitmq_username = ''
    rabbitmq_passwd = ''

    connection_name = ''
    # ---------------------------------------------------------

    try:
        opts, args = getopt.getopt(argv,"he:u:p:q:",["endpoint=","username=","passwd=","connection="])
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
        elif opt in ("-c", "--connection"):
            connection_name = arg

    if not api_endpoint.strip():
        show_usage()
        sys.exit(2)

    # call rabbitmq REST API
    url = "{}{}{}".format(api_endpoint, api_path, connection_name)
    logger.debug( "url: {}".format(url) )

    # use the credentials
    http_basic_auth_credentials = (username, passwd)

    # call rabbitmq api to get queues info
    rabbitmq_response = get_rabbitmq_response(url, http_basic_auth_credentials)

    # for bulk query of all queues, result is list type
    if isinstance(rabbitmq_response, list):
        # loop through each queue info
        for connection in rabbitmq_response:
            # output queue info to stdout to be picked up by callers of this script
            print_connection(connection)
    # else result is single dict queue
    else:
        # output queue info to stdout to be picked up by callers of this script
        print_connection(rabbitmq_response)


if __name__ == "__main__":
    main(sys.argv[1:])
