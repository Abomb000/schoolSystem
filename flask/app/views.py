import json
import os

import numpy as np
from app import app
from app import r
from app.models import Student, Grade, Course
from bson import json_util
from flask import render_template, request, jsonify, Response, send_from_directory
from flask.json import JSONEncoder
from mongoengine.base import BaseDocument
from mongoengine.queryset.base import BaseQuerySet

from flask_httpauth import HTTPBasicAuth
auth = HTTPBasicAuth()
users = {
    "admin": "admin",
    "example": "example"
}


@auth.get_password
def get_pw(username):
    if username in users:
        return users.get(username)
    return None


def MongoEngineJSONEncoder(obj):
    if isinstance(obj, BaseDocument):
        return json_util._json_convert(obj.to_mongo())
    elif isinstance(obj, BaseQuerySet):
        return json_util._json_convert(obj.as_pymongo())
    return JSONEncoder.default(obj)


@app.route("/manager")
@auth.login_required
def crud():
    return render_template("crud.html")


@app.route("/", methods=["GET", "POST", "PUT"])
def index():
    rez = r.get("topstudent")
    ti = ''
    data = None
    top_grade = []
    if not rez:
        top_grade = list(Grade.objects().aggregate(*[
            {"$group": {"_id": {"student": "$student", "course": "$course"}, "avggrade": {"$avg": "$grade"}}},
            {"$sort": {"avggrade": -1}}, {"$limit": 1}
        ]))
        if top_grade:

            student_db = Student.objects.get(id=top_grade[0]["_id"]["student"])
            top_grade[0]["name"] = student_db.firstName
            top_grade[0]["lname"] = student_db.lastName

            course_db = Course.objects.get(id=top_grade[0]["_id"]["course"])
            s = json.dumps(top_grade[0], indent=4, sort_keys=True)
            r.set("topstudent", s)
            r.expire('topstudent', 30)
            rez = r.get("topstudent")

            ti = json.dumps(MongoEngineJSONEncoder(course_db), indent=4, sort_keys=True)
            data = json.loads(rez)
    return render_template("index.html", top_student=data, loaded=ti)


@app.route("/api/<doctype>", methods=["POST"])
def students(doctype):
    if doctype == "students":
        Student(**request.form).save()
    elif doctype == "grades":
        Grade(**request.form).save()
    elif doctype == "courses":
        Course(
            name=request.form.get("name"),
            students=np.array(request.form.getlist('students[]')).tolist()
        ).save()
    else:
        return render_template('404.html', title='404'), 404
    return jsonify({'status': 'ok', 'message': "created"}), 201


@app.route("/api/<doc_type>/<doc_id>", methods=["PUT"])
def putStudents(doc_type, doc_id):
    if doc_type == "student":
        Student.objects.get(id=doc_id).update(**request.form)
    elif doc_type == "grade":
        Grade.objects.get(id=doc_id).update(**request.form)
    elif doc_type == "course":
        if len(request.form.getlist('students[]')) < 2:
            student_list = [request.form.get('students')]
        else:
            student_list = np.array(request.form.getlist('students[]')).tolist()
        Course.objects.get(id=doc_id).update(
            name=request.form.get("name"),
            students=student_list
        )
    else:
        return render_template('404.html', title='404'), 404
    return jsonify({'message': "ok"})


@app.route("/api/<doc_type>", methods=["GET"])
def readApi(doc_type):
    if doc_type == "students":
        data_set = Student.objects()
    elif doc_type == "grades":
        data_set = Grade.objects()
    elif doc_type == "courses":
        data_set = Course.objects()
    else:
        return render_template('404.html', title='404'), 404
    return json.dumps({"aaData": MongoEngineJSONEncoder(data_set)}), 200


@app.route("/api/<doc_type>/<doc_id>", methods=["GET"])
def getStudent(doc_type, doc_id):
    if doc_type == "student":
        data_set = Student.objects.get(id=doc_id)
    elif doc_type == "grade":
        data_set = Grade.objects.get(id=doc_id)
    elif doc_type == "course":
        data_set = Course.objects.get(id=doc_id)
    else:
        return render_template('404.html', title='404'), 404
    return Response("{\"aaData\":" + data_set + "}", mimetype="application/json", status=200)


@app.route("/create/<doc_type>", methods=["GET"])
def createStudent(doc_type):
    data_set = {}
    if doc_type in ['student', 'grade', 'course']:
        if doc_type == 'grade':
            data_set = {**data_set, "users": MongoEngineJSONEncoder(Student.objects())}
            data_set = {**data_set, "courses": MongoEngineJSONEncoder(Course.objects())}
        return render_template(doc_type + ".html", data=data_set, id='')
    return render_template('404.html', title='404'), 404


@app.route("/edit/<doc_type>/<doc_id>", methods=["GET"])
def editData(doc_type, doc_id):
    if doc_type == "student":
        data_set = Student.objects.get(id=doc_id)
    elif doc_type == "grade":
        data_set = dict(Grade.objects.get(id=doc_id))
        data_set = {**data_set, "users": MongoEngineJSONEncoder(Student.objects())}
    elif doc_type == "course":
        data_set = dict(MongoEngineJSONEncoder(Course.objects.get(id=doc_id)))
        data_set = {**data_set, "users": MongoEngineJSONEncoder(Student.objects())}
    else:
        return render_template('404.html', title='404'), 404

    return render_template(doc_type + ".html", data=data_set, id=doc_id)


@app.route("/api/<doctype>/<doc_id>", methods=["DELETE"])
def apiDelete(doc_type, doc_id):
    if doc_type in ['student', 'grade', 'course']:
        if doc_type == "student":
            Student.objects.get(id=doc_id).delete()
        elif doc_type == "grade":
            Grade.objects.get(id=doc_id).delete()
        elif doc_type == "course":
            Course.objects.get(id=doc_id).delete()
        return jsonify({'message': "ok"})

    return render_template('404.html', title='404'), 404


@app.route("/static/<path:path>")
def loadStatic(path):
    return send_from_directory('static', path)


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')
