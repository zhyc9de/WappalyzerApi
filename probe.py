# coding:utf-8
import time
import ujson as json

from libs.crawler.selenium import chrome_new_session
from libs.redis import model_redis, Run_Lock, List_Todo, Key_Status


def probe(page_url):
    driver, _ = chrome_new_session(extensions=['wappalyzer'])

    driver.get(page_url)

    time.sleep(2)

    driver.quit()


if __name__ == '__main__':
    while True:
        _, task_data = model_redis.blpop(List_Todo)
        task_data = json.loads(task_data)
        model_redis.set(Run_Lock, task_data['task_id'])
        model_redis.set(Key_Status.format(task_data['task_id']), json.dumps({
            'scan': 0,
            'apps': []
        }))
        list(map(probe, task_data['urls']))
        time.sleep(5)
        model_redis.delete(Run_Lock)
