from app import app
from app import r
from app.models import Student, Grade, Course
import json
import numpy as np
from flask import render_template, request, redirect, url_for, jsonify, Response, send_from_directory

from flask.json import JSONEncoder
from bson import json_util
from mongoengine.base import BaseDocument
from mongoengine.queryset.base import BaseQuerySet


def MongoEngineJSONEncoder(obj):
    if isinstance(obj, BaseDocument):
        return json_util._json_convert(obj.to_mongo())
    elif isinstance(obj, BaseQuerySet):
        return json_util._json_convert(obj.as_pymongo())
    return JSONEncoder.default(obj)


@app.route("/manager")
def crud():
    return render_template("crud.html")


@app.route("/", methods=["GET", "POST", "PUT"])
def index():
    rez = r.get("topstudent")
    loaded = 0
    if not rez:
        top_grade = list(Grade.objects().aggregate(*[{"$group": {"_id": {"student": "$student", "course": "$course"},
                                                           "avggrade": {"$avg": "$grade"}}},
                                               {"$sort": {"avggrade": -1}}, {"$limit": 1}]))[0]
        s = json.dumps(top_grade, indent=4, sort_keys=True)
        r.set("topstudent", s)
        r.expire('topstudent', 30)
        rez = r.get("topstudent")
        loaded = 1

    data = json.loads(rez)
    return render_template("index.html", hits=hits, top_student=data, loaded=loaded)


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


@app.route("/api/<doctype>/<id>", methods=["PUT"])
def putStudents(doctype, id):
    if doctype == "student":
        Student.objects.get(id=id).update(**request.form)
    elif doctype == "grade":
        Grade.objects.get(id=id).update(**request.form)
    elif doctype == "course":
        if len(request.form.getlist('students[]')) < 2:
            student_list = [request.form.get('students')]
        else:
            student_list = np.array(request.form.getlist('students[]')).tolist()
        Course.objects.get(id=id).update(
            name=request.form.get("name"),
            students=student_list
        )
    else:
        return render_template('404.html', title='404'), 404
    return jsonify({'message': "ok"})
    #return Response(jsonify({'message': "ok"}), mimetype="application/json", status=200)


@app.route("/api/<doctype>", methods=["GET"])
def readapi(doctype):
    if doctype == "students":
        dataset = Student.objects()
    elif doctype == "grades":
        dataset = Grade.objects()
    elif doctype == "courses":
        dataset = Course.objects()
    else:
        return render_template('404.html', title='404'), 404
    return json.dumps({"aaData": MongoEngineJSONEncoder(dataset)}), 200


@app.route("/api/<doctype>/<id>", methods=["GET"])
def getStudent(doctype, id):
    if doctype == "student":
        dataset = Student.objects.get(id=id)
    elif doctype == "grade":
        dataset = Grade.objects.get(id=id)
    elif doctype == "course":
        dataset = Course.objects.get(id=id)
    else:
        return render_template('404.html', title='404'), 404
    return Response("{\"aaData\":" + dataset + "}", mimetype="application/json", status=200)


@app.route("/create/<doctype>", methods=["GET"])
def createStudent(doctype):
    if doctype in ['student', 'grade', 'course']:
        return render_template(doctype + ".html", data=[], id='')
    return render_template('404.html', title='404'), 404


@app.route("/edit/<doctype>/<id>", methods=["GET"])
def editdata(doctype, id):
    if doctype == "student":
        dataset = Student.objects.get(id=id)
    elif doctype == "grade":
        dataset = Grade.objects.get(id=id)
    elif doctype == "course":
        dataset = Course.objects.get(id=id)
    else:
        return render_template('404.html', title='404'), 404
    return render_template(doctype + ".html", data=dataset, id=id)


@app.route("/api/<doctype>/<id>", methods=["DELETE"])
def apiDelete(doctype, id):
    if doctype in ['student', 'grade', 'course']:
        if doctype == "student":
            Student.objects.get(id=id).delete()
        elif doctype == "grade":
            Grade.objects.get(id=id).delete()
        elif doctype == "course":
            Course.objects.get(id=id).delete()
        return jsonify({'message': "ok"})

    return render_template('404.html', title='404'), 404

@app.route("/static/<path:path>")
def loadStatic(path):
    return send_from_directory('static', path)