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
#   rabbitmq_queue.py --endpoint="https://mozart.mycluster.hysds.io:15673" --username=guest --passwd=guest [--queue=standard_product-s1gunw-topsapp-pleiade]
#   standard_product-s1gunw-topsapp-pleiades running 0 0
#
# ---------------------------------------------------------


import logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.WARNING, format='%(asctime)s %(name)s.%(funcName)s +%(lineno)s: %(levelname)-8s [%(process)d] %(message)s')

import requests
import json

class RabbitMQ:

    # rabbitmq REST API endpoint
    # many URIs require the name of a virtual host as part of the path, since names only uniquely identify objects within a virtual host. As the default virtual host is called "/", this will need to be encoded as "%2f".
    _api_queues_path = '/api/queues/%2F/'
    _api_connections_path = '/api/connections/'

    def __init__(self, api_endpoint, username, passwd):

        # call rabbitmq REST API
        self._api_endpoint = api_endpoint

        # rabbitmq credentials
        self._http_basic_auth_credentials = (username, passwd)


    def get_queues(self, queue_name=''):
        """
        Queries RabbitMQ's REST API to get list of queues.
        @return: list of dicts
        """

        # add specific queue if given. otherwise gets all queues.
        url = "{}{}{}".format(self._api_endpoint, RabbitMQ._api_queues_path, queue_name)
        logger.debug( "calling url {} with credentials {}".format(url, self._http_basic_auth_credentials) )

        # using verify=False just in case some rabbitmq endpoint yields OpenSSL.SSL.Error: [('SSL routines', 'tls_process_server_certificate', 'certificate verify failed')]
        response = requests.get(url, auth=self._http_basic_auth_credentials, verify=False)

        # exit if error so outter scripts calling this python scripts can detect for non-zero exit code
        if response.status_code != 200:
            logger.error( "got error http {} from {}".format(url, response.status_code) )
            raise Exception( "got error http {} from {}".format(url, response.status_code) )

        logger.debug( "response: {}".format(response) )

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

        # get json stream of http response
        queues = response.json()
        # for list of queues, returns list of dicts
        # if a specific queue is given, will only return dict, and not list.

        # make sure always return list of dict
        if isinstance(queues, dict):
            queues = [queues]

        logger.debug(json.dumps(queues, indent=4, sort_keys=True))

        return queues


    @staticmethod
    def queue_to_tuple(queue):
        """
        converts a queue dict to a simpler tuple subset.
        @return: tuple (queue_name, queue_state, messages_ready, messages_unacknowledged)
        """
        queue_name = queue["name"]
        logger.debug( "queue_name: {}".format(queue_name) )

        queue_state = queue["state"]
        logger.debug( "queue_state: {}".format(queue_state) )

        messages_ready = queue["messages_ready"]
        logger.debug( "messages_ready: {}".format(messages_ready) )

        messages_unacknowledged = queue["messages_unacknowledged"]
        logger.debug( "messages_unacknowledged: {}".format(messages_unacknowledged) )

        return (queue_name, queue_state, messages_ready, messages_unacknowledged)


    def get_connections(self, connection_name=''):
        """
        Queries RabbitMQ's REST API to get list of connections.
        @return: list of dicts
        """

        # add specific connection if given. otherwise gets all connections.
        url = "{}{}{}".format(self._api_endpoint, RabbitMQ._api_connections_path, connection_name)
        logger.debug( "calling url {} with credentials {}".format(url, self._http_basic_auth_credentials) )

        # using verify=False just in case some rabbitmq endpoint yields OpenSSL.SSL.Error: [('SSL routines', 'tls_process_server_certificate', 'certificate verify failed')]
        response = requests.get(url, auth=self._http_basic_auth_credentials, verify=False)

        # exit if error so outter scripts calling this python scripts can detect for non-zero exit code
        if response.status_code != 200:
            logger.error( "got error http {} from {}".format(url, response.status_code) )
            raise Exception( "got error http {} from {}".format(url, response.status_code) )

        logger.debug( "response: {}".format(response) )

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

        # get json stream of http response
        connections = response.json()
        # for list of connections, returns list of dicts
        # if a specific connection is given, will only return dict, and not list.

        # make sure always return list of dict
        if isinstance(connections, dict):
            connections = [connections]

        logger.debug(json.dumps(connections, indent=4, sort_keys=True))

        return connections

    @staticmethod
    def connection_to_tuple(connection):
        """
        converts a connection dict to a simpler tuple subset.
        @return: tuple (connection_name, connection_state, connection_send_rate, connection_recv_rate)
        """
        connection_name = connection["name"]
        logger.debug( "connection_name: {}".format(connection_name) )

        connection_state = connection["state"]
        logger.debug( "connection_state: {}".format(connection_state) )

        connection_send_oct_details = connection["send_oct_details"]
        connection_send_rate = connection_send_oct_details["rate"]
        logger.debug( "connection_send_rate: {}".format(connection_send_rate) )

        connection_recv_oct_details = connection["recv_oct_details"]
        connection_recv_rate = connection_recv_oct_details["rate"]
        logger.debug( "connection_recv_rate: {}".format(connection_recv_rate) )

        return (connection_name, connection_state, connection_send_rate, connection_recv_rate)
