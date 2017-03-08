# coding:utf-8
from redis import StrictRedis

model_redis = StrictRedis(host='127.0.0.1', port='6379',
                          decode_responses=True)

List_Todo = 'WappalyzerApi:todo'
Key_Status = 'WappalyzerApi:status:{}'  # task_id
Run_Lock = 'WappalyzerApi:run:lock'
