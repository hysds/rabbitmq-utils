# RabbitMQ Utilities

RabbitMQ has a web UI to see real-time information about queues, connections, and workers.
This repo has tools and examples for calling the RabbitMQ REST API to query for similar information.

rabbitmq_queue_info.py
----------------------

This script calls RabbitMQ REST API to get a queue info.
Uses request module, which has been tested up to python 3.7.

input arguments:
  --endpoint: the RabbitMQ API endpoint. e.g. "https://mozart.mycluster.hysds.io:15673" see https://mozart.mycluster.hysds.io:15673/api/
  --username: username for rabbitmq
  --passwd: password for rabbitmq
  --queue: (optional) name of queue. if specified, it will only return info for this queue name. if not specified, then all queues will be shown.

outputs to stdout:
```
   <queue name> <state> <messages_ready> <messages_unacknowledged>
```

example usage of a specific queue:
```
rabbitmq_queue_info.py --endpoint="https://mozart.mycluster.hysds.io:15673" --username=mee --passwd=mypass --queue=standard_product-s1gunw-topsapp-pleiade

standard_product-s1gunw-topsapp-pleiades running 0 0
```

example usage for all queues, ignoring the "celery" ones:
```
./rabbitmq_queue_info.py --endpoint="http://mozart.mycluster.hysds.io:15673" --username=mee --passwd=mypass | grep -v celery

(mozart) hysdsops@ip-100-67-33-56:/tmp$ python rabbitmq_queue_info.py --endpoint="http://e-jobs.aria.hysds.io:15672" --username=guest --passwd=guest | grep -v celery
aria-job_worker-large running 1 0
asf-job_worker-large running 0 0
dataset_processed running 0 0
factotum-create_aoi-queue running 0 0
factotum-job_worker-apihub_scraper_throttled running 0 0
factotum-job_worker-apihub_throttled running 0 0
factotum-job_worker-asf_throttled running 0 0
factotum-job_worker-global_ipf_scrape running 0 0
factotum-job_worker-large running 0 0
factotum-job_worker-realtime running 0 0
factotum-job_worker-scihub_throttled running 0 0
factotum-job_worker-small running 0 0
factotum-job_worker-unavco_throttled running 0 0
import_prov_es running 0 0
ipf-scraper-scihub running 0 0
jobs_processed running 0 0
on_demand_dataset running 0 0
on_demand_job running 0 0
process_events_tasks running 0 0
spyddder-sling-extract-asf running 1 0
standard_product-s1gunw-topsapp-pleiades running 0 0
system-jobs-queue running 0 0
urgent-response-job_worker-large running 0 0
urgent-response-job_worker-small running 0 0
user_rules_dataset running 0 0
user_rules_job running 0 0
user_rules_trigger running 0 0
```

rabbitmq-sdswatch.sh
--------------------

This script calls the rabbitmq tool "rabbitmq_queue_info.py"
to query the job queues (ignoring celery queues) and outputs
to STDOUT log file in SDSWatch log format. THe intent to output
to STDOUT is to ease running this script under supervisord.

to use, update the settings in the script:
RABBITMQ_API_ENDPOINT="https://mozart.mycluster.hysds.io:15673"
RABBITMQ_USERNAME="meee"
RABBITMQ_PASSWD="mypass"

example of running rabbitmq-sdswatch.sh to stdout:
```
2020-04-10T23:30:21+0000 , https://mozart.mycluster.hysds.io:15673 , rabbitmq , factotum-create_aoi-queue , state, running 
2020-04-10T23:30:21+0000 , https://mozart.mycluster.hysds.io:15673 , rabbitmq , factotum-create_aoi-queue , ready, 0 
2020-04-10T23:30:21+0000 , https://mozart.mycluster.hysds.io:15673 , rabbitmq , factotum-create_aoi-queue , unacked, 0 
2020-04-10T23:30:21+0000 , https://mozart.mycluster.hysds.io:15673 , rabbitmq , factotum-job_worker-apihub_scraper_throttled , state, running 
2020-04-10T23:30:21+0000 , https://mozart.mycluster.hysds.io:15673 , rabbitmq , factotum-job_worker-apihub_scraper_throttled , ready, 0 
2020-04-10T23:30:21+0000 , https://mozart.mycluster.hysds.io:15673 , rabbitmq , factotum-job_worker-apihub_scraper_throttled , unacked, 0 
2020-04-10T23:30:21+0000 , https://mozart.mycluster.hysds.io:15673 , rabbitmq , factotum-job_worker-apihub_throttled , state, running 
2020-04-10T23:30:21+0000 , https://mozart.mycluster.hysds.io:15673 , rabbitmq , factotum-job_worker-apihub_throttled , ready, 0 
2020-04-10T23:30:21+0000 , https://mozart.mycluster.hysds.io:15673 , rabbitmq , factotum-job_worker-apihub_throttled , unacked, 0 
2020-04-10T23:30:21+0000 , https://mozart.mycluster.hysds.io:15673 , rabbitmq , factotum-job_worker-asf_throttled , state, running 
2020-04-10T23:30:21+0000 , https://mozart.mycluster.hysds.io:15673 , rabbitmq , factotum-job_worker-asf_throttled , ready, 0 
2020-04-10T23:30:21+0000 , https://mozart.mycluster.hysds.io:15673 , rabbitmq , factotum-job_worker-asf_throttled , unacked, 0 
2020-04-10T23:30:21+0000 , https://mozart.mycluster.hysds.io:15673 , rabbitmq , factotum-job_worker-global_ipf_scrape , state, running 
2020-04-10T23:30:21+0000 , https://mozart.mycluster.hysds.io:15673 , rabbitmq , factotum-job_worker-global_ipf_scrape , ready, 0 
2020-04-10T23:30:21+0000 , https://mozart.mycluster.hysds.io:15673 , rabbitmq , factotum-job_worker-global_ipf_scrape , unacked, 0 
2020-04-10T23:30:21+0000 , https://mozart.mycluster.hysds.io:15673 , rabbitmq , factotum-job_worker-large , state, running 
2020-04-10T23:30:21+0000 , https://mozart.mycluster.hysds.io:15673 , rabbitmq , factotum-job_worker-large , ready, 0 
2020-04-10T23:30:21+0000 , https://mozart.mycluster.hysds.io:15673 , rabbitmq , factotum-job_worker-large , unacked, 0 
2020-04-10T23:30:21+0000 , https://mozart.mycluster.hysds.io:15673 , rabbitmq , factotum-job_worker-realtime , state, running 
2020-04-10T23:30:21+0000 , https://mozart.mycluster.hysds.io:15673 , rabbitmq , factotum-job_worker-realtime , ready, 0 
2020-04-10T23:30:21+0000 , https://mozart.mycluster.hysds.io:15673 , rabbitmq , factotum-job_worker-realtime , unacked, 0 
2020-04-10T23:30:21+0000 , https://mozart.mycluster.hysds.io:15673 , rabbitmq , factotum-job_worker-scihub_throttled , state, running 
2020-04-10T23:30:21+0000 , https://mozart.mycluster.hysds.io:15673 , rabbitmq , factotum-job_worker-scihub_throttled , ready, 0 
2020-04-10T23:30:21+0000 , https://mozart.mycluster.hysds.io:15673 , rabbitmq , factotum-job_worker-scihub_throttled , unacked, 0 
2020-04-10T23:30:21+0000 , https://mozart.mycluster.hysds.io:15673 , rabbitmq , factotum-job_worker-small , state, running 
2020-04-10T23:30:21+0000 , https://mozart.mycluster.hysds.io:15673 , rabbitmq , factotum-job_worker-small , ready, 0 
2020-04-10T23:30:21+0000 , https://mozart.mycluster.hysds.io:15673 , rabbitmq , factotum-job_worker-small , unacked, 1 
2020-04-10T23:30:21+0000 , https://mozart.mycluster.hysds.io:15673 , rabbitmq , factotum-job_worker-unavco_throttled , state, running 
2020-04-10T23:30:21+0000 , https://mozart.mycluster.hysds.io:15673 , rabbitmq , factotum-job_worker-unavco_throttled , ready, 0 
2020-04-10T23:30:21+0000 , https://mozart.mycluster.hysds.io:15673 , rabbitmq , factotum-job_worker-unavco_throttled , unacked, 0 
```

The output can be redirected a rabbitmq.sdswatch.log file to be picked up by SDSWatch agent and sent to elasticsearch for analysis.

