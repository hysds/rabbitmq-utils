# RabbitMQ Utilities

RabbitMQ has a web UI to see real-time information about queues, connections, and workers.
This repo has tools and examples for calling the RabbitMQ REST API to query for similar information.

Queues
======

rabbitmq_queue_monitor.py
-------------------------

This script calls RabbitMQ REST API to get a queue info.
Uses request module, which has been tested up to python 3.7.

input arguments:
   --endpoint: the RabbitMQ API endpoint. e.g. "https://mozart.mycluster.hysds.io:15673" see http://e-jobs.aria.hysds.io:15672/api/
   --username: username for rabbitmq
   --passwd: password for rabbitmq
   --queue: (optional) name of queue. if specified, it will only return info for this queue name. if not specified, then all queues will be shown.
   --interval: (optional) frequency of how often to check rabbitmq in unit seconds. (default=10)


outputs to stdout:
```
   timestamp, queue_name, queue_state, messages_ready, messages_unacknowledged
```

example usage of a specific queue:
```
$ ./rabbitmq_queue_monitor.py --endpoint="https://mozart.mycluster.hysds.io:15673" --username=guest --passwd=guest --queue=user_rules_dataset --interval=10

2020-05-21T22:37:29+00:00 user_rules_dataset running 0 0
```

example usage for all queues:
```
$ ./rabbitmq_queue_monitor.py --endpoint="https://mozart.mycluster.hysds.io:15673" --username=guest --passwd=guest --interval=10
2020-05-21T22:37:29+00:00 aria-job_worker-large running 1 0
2020-05-21T22:37:29+00:00 asf-job_worker-large running 0 0
2020-05-21T22:37:29+00:00 dataset_processed running 0 0
2020-05-21T22:37:29+00:00 factotum-create_aoi-queue running 0 0
2020-05-21T22:37:29+00:00 factotum-job_worker-apihub_scraper_throttled running 0 0
2020-05-21T22:37:29+00:00 factotum-job_worker-apihub_throttled running 0 0
2020-05-21T22:37:29+00:00 factotum-job_worker-asf_throttled running 0 0
2020-05-21T22:37:29+00:00 factotum-job_worker-global_ipf_scrape running 0 0
2020-05-21T22:37:29+00:00 factotum-job_worker-large running 0 0
2020-05-21T22:37:29+00:00 factotum-job_worker-realtime running 0 0
2020-05-21T22:37:29+00:00 factotum-job_worker-scihub_throttled running 0 0
2020-05-21T22:37:29+00:00 factotum-job_worker-small running 0 0
2020-05-21T22:37:29+00:00 factotum-job_worker-unavco_throttled running 0 0
2020-05-21T22:37:29+00:00 import_prov_es running 0 0
2020-05-21T22:37:29+00:00 ipf-scraper-scihub running 0 0
2020-05-21T22:37:29+00:00 jobs_processed running 0 0
2020-05-21T22:37:29+00:00 on_demand_dataset running 0 0
2020-05-21T22:37:29+00:00 on_demand_job running 0 0
2020-05-21T22:37:29+00:00 process_events_tasks running 0 0
2020-05-21T22:37:29+00:00 spyddder-sling-extract-asf running 1 0
2020-05-21T22:37:29+00:00 standard_product-s1gunw-topsapp-pleiades running 0 0
2020-05-21T22:37:29+00:00 system-jobs-queue running 0 0
2020-05-21T22:37:29+00:00 urgent-response-job_worker-large running 0 0
2020-05-21T22:37:29+00:00 urgent-response-job_worker-small running 0 0
2020-05-21T22:37:29+00:00 user_rules_dataset running 0 0
2020-05-21T22:37:29+00:00 user_rules_job running 0 0
2020-05-21T22:37:29+00:00 user_rules_trigger running 0 0
```

rabbitmq_queue_monitor_to_sdswatch.sh
-------------------------------------

This script calls the rabbitmq tool "rabbitmq_queue_monitor.py"
to query the job queues (ignoring celery queues) and outputs
to STDOUT log file in SDSWatch log format.

To use, update the settings in the script:
RABBITMQ_API_ENDPOINT="https://mozart.mycluster.hysds.io:15673"
RABBITMQ_USERNAME="username"
RABBITMQ_PASSWD="mypasswd"

Example output:
```
2020-05-22T03:18:03+00:00 , https://100.100.100.100:15673 , rabbitmq.queue , jobs_processed , state, running
2020-05-22T03:18:03+00:00 , https://100.100.100.100:15673 , rabbitmq.queue , jobs_processed , ready, 0
2020-05-22T03:18:03+00:00 , https://100.100.100.100:15673 , rabbitmq.queue , jobs_processed , unacked, 0
2020-05-22T03:19:04+00:00 , https://100.100.100.100:15673 , rabbitmq.queue , jobs_processed , state, running
2020-05-22T03:19:04+00:00 , https://100.100.100.100:15673 , rabbitmq.queue , jobs_processed , ready, 0
2020-05-22T03:19:04+00:00 , https://100.100.100.100:15673 , rabbitmq.queue , jobs_processed , unacked, 1
2020-05-22T03:19:04+00:00 , https://100.100.100.100:15673 , rabbitmq.queue , urgent-response-job_worker-large , state, running
2020-05-22T03:19:04+00:00 , https://100.100.100.100:15673 , rabbitmq.queue , urgent-response-job_worker-large , ready, 12349
2020-05-22T03:19:04+00:00 , https://100.100.100.100:15673 , rabbitmq.queue , urgent-response-job_worker-large , unacked, 0
2020-05-22T03:20:04+00:00 , https://100.100.100.100:15673 , rabbitmq.queue , urgent-response-job_worker-large , state, running
2020-05-22T03:20:04+00:00 , https://100.100.100.100:15673 , rabbitmq.queue , urgent-response-job_worker-large , ready, 13090
2020-05-22T03:20:04+00:00 , https://100.100.100.100:15673 , rabbitmq.queue , urgent-response-job_worker-large , unacked, 0

```

The output can be redirected a rabbitmq.sdswatch.log file to be picked up by SDSWatch agent and sent to elasticsearch for analysis.

Connections
===========

rabbitmq_connection_monitor.py
------------------------------

This script calls RabbitMQ REST API to get a connection info.
Uses request module, which has been tested up to python 3.7.

input arguments:
   --endpoint: the RabbitMQ API endpoint. e.g. "https://mozart.mycluster.hysds.io:15673" see http://e-jobs.aria.hysds.io:15672/api/
   --username: username for rabbitmq
   --passwd: password for rabbitmq
   --connection: (optional) name of connection. if specified, it will only return info for this queue name. if not specified, then all connections will be shown.
                 format of this string is "127.0.0.1:46542 -> 127.0.0.1:5672"
   --interval: (optional) frequency of how often to check rabbitmq in unit seconds. (default=10)

outputs to stdout:
```
timestamp, connection_name, connection_state, connection_send_rate, connection_recv_rate
```
note that
* the connection_name is:  "client_host:client_port -> server_host:server_port"
* send/receive rates are in B/s units.

example usage:
```
$ ./rabbitmq_connection_monitor.py --endpoint="https://mozart.mycluster.hysds.io:15673" --username=guest --passwd=guest [--connection="127.0.0.1:46542 -> 127.0.0.1:5672"]
# 2020-05-22T02:24:32+00:00 , https://100.100.100.100:15673 , rabbitmq.connection , 127.0.0.1:41446->127.0.0.1:5672 , state, running 
# 2020-05-22T02:24:32+00:00 , https://100.100.100.100:15673 , rabbitmq.connection , 127.0.0.1:41446->127.0.0.1:5672 , send_rate_to_client, 45.6 
# 2020-05-22T02:24:32+00:00 , https://100.100.100.100:15673 , rabbitmq.connection , 127.0.0.1:41446->127.0.0.1:5672 , recv_rate_from_client, 0.0 
# 2020-05-22T02:24:32+00:00 , https://100.100.100.100:15673 , rabbitmq.connection , 127.0.0.1:41454->127.0.0.1:5672 , state, running 
# 2020-05-22T02:24:32+00:00 , https://100.100.100.100:15673 , rabbitmq.connection , 127.0.0.1:41454->127.0.0.1:5672 , send_rate_to_client, 0.0 
# 2020-05-22T02:24:32+00:00 , https://100.100.100.100:15673 , rabbitmq.connection , 127.0.0.1:41454->127.0.0.1:5672 , recv_rate_from_client, 0.0 

```

rabbitmq_connection_monitor_to_sdswatch.sh
------------------------------------------

This script calls the rabbitmq tool "rabbitmq_connection_monitor.py"
to query the rabbitmq connection and outputs to STDOUT log file in SDSWatch log format.

To use, update the settings in the script:
RABBITMQ_API_ENDPOINT="https://mozart.mycluster.hysds.io:15673"
RABBITMQ_USERNAME="username"
RABBITMQ_PASSWD="mypasswd"

example of running rabbitmq_connection-sdswatch.sh to stdout:
```
2020-04-14T22:06:52+0000 , https://100.100.100.100:15673 , rabbitmq.connection , 127.0.0.1:46512->127.0.0.1:5672 , send_rate_to_client, 45.6 
2020-04-14T22:06:52+0000 , https://100.100.100.100:15673 , rabbitmq.connection , 127.0.0.1:46512->127.0.0.1:5672 , recv_rate_from_client, 0.0 
2020-04-14T22:06:52+0000 , https://100.100.100.100:15673 , rabbitmq.connection , 127.0.0.1:46514->127.0.0.1:5672 , state, running 
2020-04-14T22:06:52+0000 , https://100.100.100.100:15673 , rabbitmq.connection , 127.0.0.1:46514->127.0.0.1:5672 , send_rate_to_client, 45.6 
2020-04-14T22:06:52+0000 , https://100.100.100.100:15673 , rabbitmq.connection , 127.0.0.1:46514->127.0.0.1:5672 , recv_rate_from_client, 0.0 
2020-04-14T22:06:52+0000 , https://100.100.100.100:15673 , rabbitmq.connection , 127.0.0.1:46516->127.0.0.1:5672 , state, running 
2020-04-14T22:06:52+0000 , https://100.100.100.100:15673 , rabbitmq.connection , 127.0.0.1:46516->127.0.0.1:5672 , send_rate_to_client, 0.0 
2020-04-14T22:06:52+0000 , https://100.100.100.100:15673 , rabbitmq.connection , 127.0.0.1:46516->127.0.0.1:5672 , recv_rate_from_client, 0.0 
2020-04-14T22:06:52+0000 , https://100.100.100.100:15673 , rabbitmq.connection , 127.0.0.1:46518->127.0.0.1:5672 , state, running 
2020-04-14T22:06:52+0000 , https://100.100.100.100:15673 , rabbitmq.connection , 127.0.0.1:46518->127.0.0.1:5672 , send_rate_to_client, 45.6 
2020-04-14T22:06:52+0000 , https://100.100.100.100:15673 , rabbitmq.connection , 127.0.0.1:46518->127.0.0.1:5672 , recv_rate_from_client, 0.0 
2020-04-14T22:06:52+0000 , https://100.100.100.100:15673 , rabbitmq.connection , 127.0.0.1:46520->127.0.0.1:5672 , state, running 
2020-04-14T22:06:52+0000 , https://100.100.100.100:15673 , rabbitmq.connection , 127.0.0.1:46520->127.0.0.1:5672 , send_rate_to_client, 45.6 
2020-04-14T22:06:52+0000 , https://100.100.100.100:15673 , rabbitmq.connection , 127.0.0.1:46520->127.0.0.1:5672 , recv_rate_from_client, 0.0 
2020-04-14T22:06:52+0000 , https://100.100.100.100:15673 , rabbitmq.connection , 127.0.0.1:46522->127.0.0.1:5672 , state, running 
2020-04-14T22:06:52+0000 , https://100.100.100.100:15673 , rabbitmq.connection , 127.0.0.1:46522->127.0.0.1:5672 , send_rate_to_client, 0.0 
2020-04-14T22:06:52+0000 , https://100.100.100.100:15673 , rabbitmq.connection , 127.0.0.1:46522->127.0.0.1:5672 , recv_rate_from_client, 0.0 
2020-04-14T22:06:52+0000 , https://100.100.100.100:15673 , rabbitmq.connection , 127.0.0.1:46524->127.0.0.1:5672 , state, running 
2020-04-14T22:06:52+0000 , https://100.100.100.100:15673 , rabbitmq.connection , 127.0.0.1:46524->127.0.0.1:5672 , send_rate_to_client, 0.0 
2020-04-14T22:06:52+0000 , https://100.100.100.100:15673 , rabbitmq.connection , 127.0.0.1:46524->127.0.0.1:5672 , recv_rate_from_client, 0.0 
2020-04-14T22:06:52+0000 , https://100.100.100.100:15673 , rabbitmq.connection , 127.0.0.1:46526->127.0.0.1:5672 , state, running 
2020-04-14T22:06:52+0000 , https://100.100.100.100:15673 , rabbitmq.connection , 127.0.0.1:46526->127.0.0.1:5672 , send_rate_to_client, 45.6 
2020-04-14T22:06:52+0000 , https://100.100.100.100:15673 , rabbitmq.connection , 127.0.0.1:46526->127.0.0.1:5672 , recv_rate_from_client, 0.0 
2020-04-14T22:06:52+0000 , https://100.100.100.100:15673 , rabbitmq.connection , 127.0.0.1:46528->127.0.0.1:5672 , state, running 
2020-04-14T22:06:52+0000 , https://100.100.100.100:15673 , rabbitmq.connection , 127.0.0.1:46528->127.0.0.1:5672 , send_rate_to_client, 0.0 
2020-04-14T22:06:52+0000 , https://100.100.100.100:15673 , rabbitmq.connection , 127.0.0.1:46528->127.0.0.1:5672 , recv_rate_from_client, 0.0 
2020-04-14T22:06:52+0000 , https://100.100.100.100:15673 , rabbitmq.connection , 127.0.0.1:46530->127.0.0.1:5672 , state, running 
2020-04-14T22:06:52+0000 , https://100.100.100.100:15673 , rabbitmq.connection , 127.0.0.1:46530->127.0.0.1:5672 , send_rate_to_client, 0.0 
2020-04-14T22:06:52+0000 , https://100.100.100.100:15673 , rabbitmq.connection , 127.0.0.1:46530->127.0.0.1:5672 , recv_rate_from_client, 0.0 
2020-04-14T22:06:52+0000 , https://100.100.100.100:15673 , rabbitmq.connection , 127.0.0.1:46532->127.0.0.1:5672 , state, running 
2020-04-14T22:06:52+0000 , https://100.100.100.100:15673 , rabbitmq.connection , 127.0.0.1:46532->127.0.0.1:5672 , send_rate_to_client, 0.0 
2020-04-14T22:06:52+0000 , https://100.100.100.100:15673 , rabbitmq.connection , 127.0.0.1:46532->127.0.0.1:5672 , recv_rate_from_client, 0.0 
2020-04-14T22:06:52+0000 , https://100.100.100.100:15673 , rabbitmq.connection , 127.0.0.1:46534->127.0.0.1:5672 , state, running 
2020-04-14T22:06:52+0000 , https://100.100.100.100:15673 , rabbitmq.connection , 127.0.0.1:46534->127.0.0.1:5672 , send_rate_to_client, 0.0 
2020-04-14T22:06:52+0000 , https://100.100.100.100:15673 , rabbitmq.connection , 127.0.0.1:46534->127.0.0.1:5672 , recv_rate_from_client, 0.0 
2020-04-14T22:06:52+0000 , https://100.100.100.100:15673 , rabbitmq.connection , 127.0.0.1:46536->127.0.0.1:5672 , state, running 
2020-04-14T22:06:52+0000 , https://100.100.100.100:15673 , rabbitmq.connection , 127.0.0.1:46536->127.0.0.1:5672 , send_rate_to_client, 0.0 
2020-04-14T22:06:52+0000 , https://100.100.100.100:15673 , rabbitmq.connection , 127.0.0.1:46536->127.0.0.1:5672 , recv_rate_from_client, 0.0 
2020-04-14T22:06:52+0000 , https://100.100.100.100:15673 , rabbitmq.connection , 127.0.0.1:46538->127.0.0.1:5672 , state, running 
2020-04-14T22:06:52+0000 , https://100.100.100.100:15673 , rabbitmq.connection , 127.0.0.1:46538->127.0.0.1:5672 , send_rate_to_client, 0.0 
2020-04-14T22:06:52+0000 , https://100.100.100.100:15673 , rabbitmq.connection , 127.0.0.1:46538->127.0.0.1:5672 , recv_rate_from_client, 0.0 
2020-04-14T22:06:52+0000 , https://100.100.100.100:15673 , rabbitmq.connection , 127.0.0.1:46540->127.0.0.1:5672 , state, running 
2020-04-14T22:06:52+0000 , https://100.100.100.100:15673 , rabbitmq.connection , 127.0.0.1:46540->127.0.0.1:5672 , send_rate_to_client, 45.6 
2020-04-14T22:06:52+0000 , https://100.100.100.100:15673 , rabbitmq.connection , 127.0.0.1:46540->127.0.0.1:5672 , recv_rate_from_client, 0.0 
2020-04-14T22:06:52+0000 , https://100.100.100.100:15673 , rabbitmq.connection , 127.0.0.1:46542->127.0.0.1:5672 , state, running 
2020-04-14T22:06:52+0000 , https://100.100.100.100:15673 , rabbitmq.connection , 127.0.0.1:46542->127.0.0.1:5672 , send_rate_to_client, 0.0 
2020-04-14T22:06:52+0000 , https://100.100.100.100:15673 , rabbitmq.connection , 127.0.0.1:46542->127.0.0.1:5672 , recv_rate_from_client, 0.0 
```

