from flask import Flask, request, jsonify
from flask_cors import CORS
import threading
import time
import uuid
from peter import Assistant

app = Flask(__name__)
CORS(app)

peter = Assistant.create_with_default_name()

daemon_thread = threading.Thread(target=peter.serve, daemon=True)

daemon_thread.start()

@app.route('/dialogue', methods=['POST'])
def dialogue():
    data = request.json.get('data')
    if not data:
        return jsonify({'error':'Data is required'}), 400

    task_id = str(uuid.uuid4())
    print("dialogue input data:%s"%data)
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
    #print("Headers:", request.headers)
    print("Request Data:", request.data)
    print("Request JSON:", request.json)
    data = request.json
    if not isinstance(data, dict):
        return jsonify({'error': 'Invalid JSON data'}), 400
    if 'title' in data:
        print("Adding task with title:", data['title'])
        # 目前默认都是 解析是否是学习某一主题，然后添加的都是 TeacherTask
        # TODO 后面需要考虑重新设计
        try:
            int_uid = int(data["userID"])
        except:
            return jsonify({'error': 'userID is not int'}), 400
        peter.add_task(3, title=data['title'], uid=int_uid) #
        print("Task added successfully")
    else:
        return jsonify({'error': 'Title is missing'}), 400
    return jsonify({'message': '确认成功'}), 200

@app.route('/check', methods=['POST'])
def check_message():
    #for key, value in peter.task_manager.taskMessage.items():
    #print("Request Data:", request.data)
    print("Request JSON:", request.json)
    try:
        uid = int(request.json['userID'])

        if uid in peter.task_manager.taskMessages:
            http_code = 200
            ret_json = peter.task_manager.taskMessages[uid]
            print(ret_json)
        else:
            http_code = 201
            ret_json = {'message':"No tasks"}
    except Exception as e:
        http_code = 401
        print("flask server 77" + str(e))
        ret_json = {'message':"unexpted error, 76"}
    return jsonify(ret_json), http_code

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False, host='0.0.0.0', port=5001)
