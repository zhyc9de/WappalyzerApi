# coding:utf-8
import random
import string
import time
import ujson as json

from sanic import Sanic
from sanic.response import text

from libs.redis import model_redis, Run_Lock, Key_Status, List_Todo

app = Sanic()


def remove_duplicates(target_list):
    key_set = set()
    ret_list = []
    for target in target_list:
        unique_key = target['app'] + ':' + target['version']
        if unique_key not in key_set:
            ret_list.append(target)
            key_set.add(unique_key)
    return ret_list


@app.route("/", methods=['POST'])
async def receive(request):
    data = json.loads(request.form['json'][0])['appsDetected']

    insert_data_list = list(map(lambda d: {
        'app': d['app'],
        'version': d['version']
    }, data.values()))

    task_id = model_redis.get(Run_Lock)
    task_key = Key_Status.format(task_id)

    old_data = model_redis.get(task_key)

    old_data = json.loads(old_data)
    old_data['scan'] += 1
    insert_data_list += old_data['apps']
    old_data['apps'] = remove_duplicates(insert_data_list)

    model_redis.set(task_key, json.dumps(old_data))

    return text('')


@app.route("/task", methods=['POST'])
async def task(request):
    urls = request.form['urls']
    task_id = str(time.time()) + ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(3))
    model_redis.lpush(List_Todo, json.dumps({
        'task_id': task_id,
        'urls': urls
    }))
    return text(task_id)


@app.route("/status/<task_id>")
async def status(request, task_id):
    from sanic.response import json as jsonify
    task_key = Key_Status.format(task_id)

    data = model_redis.get(task_key)
    if data:
        return jsonify(json.loads(data))
    else:
        return jsonify({})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
