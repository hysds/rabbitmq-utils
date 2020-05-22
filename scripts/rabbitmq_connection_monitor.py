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
#   --interval: (optional) frequency of how often to check rabbitmq in unit seconds. (default=10)
#
# outputs to stdout:
#   timestamp, connection_name, connection_state, connection_send_rate, connection_recv_rate
# note that
#   * the connection_name is:  "client_host:client_port -> server_host:server_port"
#   * send/receive rates are in B/s units.
#
# example usage:
# rabbitmq_connection_monitor.py --endpoint="https://mozart.mycluster.hysds.io:15673" --username=guest --passwd=guest [--connection="127.0.0.1:46542 -> 127.0.0.1:5672"]
# 2020-05-22T02:24:32+00:00 , https://100.67.33.56:15673 , rabbitmq.connection , 127.0.0.1:41446->127.0.0.1:5672 , state, running 
# 2020-05-22T02:24:32+00:00 , https://100.67.33.56:15673 , rabbitmq.connection , 127.0.0.1:41446->127.0.0.1:5672 , send_rate_to_client, 45.6 
# 2020-05-22T02:24:32+00:00 , https://100.67.33.56:15673 , rabbitmq.connection , 127.0.0.1:41446->127.0.0.1:5672 , recv_rate_from_client, 0.0 
# 2020-05-22T02:24:32+00:00 , https://100.67.33.56:15673 , rabbitmq.connection , 127.0.0.1:41454->127.0.0.1:5672 , state, running 
# 2020-05-22T02:24:32+00:00 , https://100.67.33.56:15673 , rabbitmq.connection , 127.0.0.1:41454->127.0.0.1:5672 , send_rate_to_client, 0.0 
# 2020-05-22T02:24:32+00:00 , https://100.67.33.56:15673 , rabbitmq.connection , 127.0.0.1:41454->127.0.0.1:5672 , recv_rate_from_client, 0.0 

#
# ---------------------------------------------------------

import logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.WARNING, format='%(asctime)s %(name)s.%(funcName)s +%(lineno)s: %(levelname)-8s [%(process)d] %(message)s')


# ---------------------------------------------------------

def show_usage():
    print('Usage:\n')
    print('rabbitmq_connection_monitor.py --endpoint="https://mozart.mycluster.hysds.io:15673" --username=guest --passwd=guest [--connection=] \n' )


import sys, getopt

def main(argv):

    # ---------------------------------------------------------
    # initialize constants

    # rabbitmq credentials
    rabbitmq_username = ''
    rabbitmq_passwd = ''

    api_endpoint = ''
    connection_name = ''
    interval = 10

    # ---------------------------------------------------------

    try:
        opts, args = getopt.getopt(argv,"he:u:p:c:i:",["endpoint=","username=","passwd=","connection=","interval="])
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
        elif opt in ("-i", "--interval"):
            interval = int(arg)

    # check if non-null string
    if not api_endpoint.strip():
        show_usage()
        sys.exit(2)

    from rabbitmq.RabbitMQ import RabbitMQ
    rbmq = RabbitMQ(api_endpoint, username, passwd)

    import sys
    import time
    from datetime import datetime

    previous = set()
    while True:
        # timestamp of query
        now = datetime.now().astimezone().replace(microsecond=0).isoformat()

        # query rabbitmq for latest connection state
        connections_list = rbmq.get_connections(connection_name)

        current = set()
        for connection_item in connections_list:
            # (connection_name, connection_state, connection_channels, connection_send_rate, connection_recv_rate)
            connection_tuple = RabbitMQ.connection_to_tuple(connection_item)
            current.add(connection_tuple)
        # end for
        #print("current: {}".format(current))

        # new that is not in old
        new = current.difference(previous)
        logger.debug("new: {}".format(new))

        # old that is not in new
        old = previous.difference(current)
        logger.debug("old: {}".format(old))

        # output only new changes
        for i in new:
            # output tokens: timestamp, connection_name, connection_state, connection_send_rate, connection_recv_rate
            # since we use the output in wrapper script to stream and convert to sdswatch,
            # we need to ensure that it is it does not wait until default stdout buffer filled before flushing.
            # so specifically flush after write.
            # https://www.turnkeylinux.org/blog/unix-buffering
            sys.stdout.write("{} {} {} {} {}\n".format(now, i[0], i[1], i[2], i[3]))
            sys.stdout.flush()
        # end for

        previous = current

        time.sleep(interval)
    # end while
# end main

if __name__ == "__main__":
    main(sys.argv[1:])
