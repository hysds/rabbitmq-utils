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
#   --interval: (optional) frequency of how often to check rabbitmq in unit seconds. (default=10)
#
# outputs to stdout:
#   timestamp, queue_name, queue_state, messages_ready, messages_unacknowledged
#
# example usage:
#   rabbitmq_queue.py --endpoint="https://mozart.mycluster.hysds.io:15673" --username=guest --passwd=guest [--queue=standard_product-s1gunw-topsapp-pleiade]
#   2020-05-21T22:37:29+00:00 user_rules_dataset running 0 0
#
# ---------------------------------------------------------


import logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(name)s.%(funcName)s +%(lineno)s: %(levelname)-8s [%(process)d] %(message)s')


# ---------------------------------------------------------

def show_usage():
    print('Usage:\n')
    print('rabbitmq_queue_monitor.py --endpoint="https://mozart.mycluster.hysds.io:15673" --username=guest --passwd=guest [--queue=standard_product-s1gunw-topsapp-pleiade] \n' )


import sys, getopt

def main(argv):

    # ---------------------------------------------------------
    # initialize constants

    # rabbitmq credentials
    rabbitmq_username = ''
    rabbitmq_passwd = ''

    api_endpoint = ''
    queue_name = ''
    interval = 10

    # ---------------------------------------------------------

    try:
        opts, args = getopt.getopt(argv,"he:u:p:q:i:",["endpoint=","username=","passwd=","queue=","interval="])
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

        # query rabbitmq for latest queue state
        queues_list = rbmq.get_queues(queue_name)

        current = set()
        for queue_item in queues_list:
            # (queue_name, queue_state, messages_ready, messages_unacknowledged)
            queue_tuple = RabbitMQ.queue_to_tuple(queue_item)

            # skip queue names that start with celery as low-level
            if queue_tuple[0].startswith("celery"):
                continue

            current.add(queue_tuple)
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
            # output tokens: timestamp, queue_name, queue_state, messages_ready, messages_unacknowledged
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
