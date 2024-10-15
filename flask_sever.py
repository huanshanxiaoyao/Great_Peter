from flask import Flask, request, jsonify
from flask_cors import CORS
import threading
import time
import uuid
from peter import Assistant

app = Flask(__name__)
CORS(app)

peter = Assistant.create_with_default_name()

lock = threading.Lock()

daemon_thread = threading.Thread(target=peter.serve, daemon=True)

daemon_thread.start()

@app.route('/dialogue', methods=['POST'])
def dialogue():
    print("in dialogue")
    data = request.json.get('data')
    if not data:
        return jsonify({'error':'Data is required'}), 400
    print("in dialogue")

    task_id = str(uuid.uuid4())
    ret, ret_str = peter.answer(data)
    if ret:
        ret_data = { 'need_confirm':True, \
                'confirm_str':"请确认学习内容为: "+ret_str, \
                'ssid':task_id, \
                'title':ret_str}
        http_code = 200
    else:
        ret_data = {'error':ret_str, 'ssid':task_id}
        http_code = 400
    print("ret:%d, info:%s"%(http_code, ret_str))
    return jsonify(ret_data), http_code

@app.route('/confirm', methods=['POST'])
def confirm_task():
    print("in Confirm")
    print("Headers:", request.headers)
    print("Request Data:", request.data)
    print("Request JSON:", request.json)
    data = request.json
    if not isinstance(data, dict):
        return jsonify({'error': 'Invalid JSON data'}), 400
    if 'title' in data:
        print("Adding task with title:", data['title'])
        peter.add_task(3, name=data['title'])
        print("Task added successfully")
    else:
        return jsonify({'error': 'Title is missing'}), 400
    return jsonify({'message': '确认成功'}), 200


if __name__ == '__main__':
    app.run(debug=True, use_reloader=False, host='0.0.0.0', port=5001)
