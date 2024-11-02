from flask import Flask, request, jsonify
from flask_cors import CORS
import threading
import time
import uuid
from peter import Assistant
from log_config import logger

app = Flask(__name__)
CORS(app)

peter = Assistant.create_with_default_name()

daemon_thread = threading.Thread(target=peter.serve, daemon=True)

daemon_thread.start()

@app.route('/dialogue', methods=['POST', 'GET'])
def dialogue():
    data = request.json.get('data')
    if not data:
        return jsonify({'error':'Data is required'}), 400

    task_id = str(uuid.uuid4())
    logger.info("dialogue input data:%s", data)
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
    logger.info("ret:%d, info:%s", http_code, ret_str)
    return jsonify(ret_data), http_code

@app.route('/confirm', methods=['POST', 'GET'])
def confirm_task():
    logger.info("Request Data: %s", request.json)
    data = request.json
    if not isinstance(data, dict):
        return jsonify({'error': 'Invalid JSON data'}), 400
    if 'title' in data:
        logger.info("Adding task with title: %s", data['title'])
        # 目前默认都是 解析是否是学习某一主题，然后添加的都是 TeacherTask
        # TODO 后面需要考虑重新设计
        try:
            int_uid = int(data["userID"])
        except:
            logger.error("userID is not int")
            return jsonify({'error': 'userID is not int'}), 400
        peter.add_task(3, title=data['title'], uid=int_uid) #
        logger.info("Task added successfully")
    else:
        return jsonify({'error': 'unexpected confirm data'}), 401
    return jsonify({'message': '确认成功'}), 200

@app.route('/check', methods=['POST', 'GET'])
def check_message():
    logger.info("Request JSON: %s", request.json)
    try:
        uid = int(request.json['userID'])

        if uid in peter.task_manager.taskMessages:
            http_code = 200
            ret_json = peter.task_manager.taskMessages[uid]
            logger.info(ret_json)
            with peter.task_manager.lock:
                del peter.task_manager.taskMessages[uid]
        else:
            http_code = 201
            ret_json = {'message':"No tasks"}
    except Exception as e:
        http_code = 401
        logger.error("flask server %s", str(e))
        ret_json = {'message':"unexpted error"}
    return jsonify(ret_json), http_code

@app.route('/study', methods=['POST', 'GET'])
def study():
    data = request.json
    if not isinstance(data, dict):
        return jsonify({'error': 'Invalid JSON data'}), 400
    logger.info("study request: %s"%data)
    
    try:
        uid = int(data.get('userID'))
        course_id = int(data.get('courseID'))
        outlineitem_id = int(data.get('outlineitemID'))
    except (ValueError, TypeError):
        logger.error("Invalid data types for userID, courseID, or outlineitem_id")
        return jsonify({'error': 'Invalid data types for userID, courseID, or outlineitem_id'}), 400
    
    if uid not in peter.user2taskid:
        logger.error("user not in user2taskid")
        return jsonify({'error': 'user not in task list'}), 400
    task_ids = peter.user2taskid[uid]
    if course_id not in task_ids: ## 目前 taskid 也就是 courseid , Task 和 Course是一对一，有点奇怪
        logger.error("course not in task list")
        return jsonify({'error': 'course not in task list'}), 400

    task = peter.task_manager.id2task[course_id]
    ret, info = task.study_hour(outlineitem_id)

    if not ret:
        logger.error("ret :%s"%info)
        return jsonify({'error': info}), 400

    json_data = jsonify({
        'content': info,
        'courseID': course_id,
        'outlineitem_id': outlineitem_id })
    print(json_data)
    return json_data, 200

@app.route('/delete', methods=['POST', 'GET'])
def delete_course():
    data = request.json
    if not isinstance(data, dict):
        return jsonify({'error': 'Invalid JSON data'}), 400
    logger.info("delete request: %s"%data)
    
    try:
        uid = int(data.get('userID'))
        course_id = int(data.get('courseID'))
    except (ValueError, TypeError):
        return jsonify({'error': 'Invalid data types for userID or courseID'}), 400
    
    # 检查用户是否存在
    if uid not in peter.user2taskid:
        return jsonify({'error': 'User not found'}), 404
    
    # 检查课程是否属于该用户
    if course_id not in peter.user2taskid[uid]:
        return jsonify({'error': 'Course not found for this user'}), 404
    
    # 从 user2taskid 中移除课程
    peter.user2taskid[uid].remove(course_id)
    if not peter.user2taskid[uid]:  # 如果用户没有其他课程了
        del peter.user2taskid[uid]
    
    # 从 task_manager 中移除任务
    if course_id in peter.task_manager.id2task:
        del peter.task_manager.id2task[course_id]
        logger.info(f"Deleted course {course_id} for user {uid}")
        return jsonify({'message': 'Course deleted successfully'}), 200
    else:
        logger.error(f"Course {course_id} not found in task_manager for user {uid}")
        return jsonify({'error': 'Course not found in task manager'}), 500

@app.route('/courselist', methods=['POST', 'GET'])
def get_course_list():
    data = request.json
    if not isinstance(data, dict):
        return jsonify({'error': 'Invalid JSON data'}), 400
    
    logger.info("courselist request: %s"%data)
    try:
        uid = int(data.get('userID'))
    except (ValueError, TypeError):
        return jsonify({'error': 'Invalid data type for userID'}), 400
    
    # 检查用户是否存在
    if uid not in peter.user2taskid:
        return jsonify({'error': 'User not found'}), 404
    
    # 获取用户的所有课程ID
    course_ids = peter.user2taskid[uid]
    courses_data = []
    
    # 获取每个课程的详细信息
    for course_id in course_ids:
        if course_id in peter.task_manager.id2task:
            task = peter.task_manager.id2task[course_id]
            chapters_info = []
            if task.course and task.course.chapters:
                for chapter in task.course.chapters:
                    chapter_info = {
                        'title': chapter.title,
                        'content': chapter.content,
                        'status': chapter.status
                    }
                    chapters_info.append(chapter_info)
            
            course_info = {
                'courseID': course_id,
                'title': task.name,
                'chapters': chapters_info
            }
            courses_data.append(course_info)
    
    logger.info(f"Retrieved course list for user {uid}, found {len(courses_data)} courses")
    return jsonify({
        'data': courses_data,
        'message': 'Course list retrieved successfully'
    }), 200

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False, host='0.0.0.0', port=5001)
