from flask import Flask
from flask import render_template
from flask import jsonify
from flask import request

import requests
import json

app = Flask(__name__)

with open('catalog.json', 'r') as file:
  catalog = json.load(file)

@app.route('/')
@app.route('/home')
def home():
  return render_template('views/home.html')

@app.route('/learn')
def learn():
  return render_template('views/learn.html')

@app.route('/learn/lesson/<id>')
def learn_lesson(id):
  length = len(catalog['lessons'][id]['content'])
  return render_template('views/lesson.html', data = {'id': id, 'length': length})

@app.route('/quiz')
def quiz():
  return render_template('views/quiz.html')

@app.route('/quiz/multiple/<id>')
def quiz_multiple(id):
  content = catalog['quizzes']['multiple'][id]['content']
  return render_template('views/multiple.html', data = {'id': id, 'content': content})

@app.route('/quiz/write/<id>')
def quiz_write(id):
  content = catalog['quizzes']['write'][id]['content'][0]
  return render_template('views/write.html', data = {'id': id, 'content': content})

@app.route('/api/lesson/overview/<id>')
def api_lesson_overview(id):
  overview = {
    "lessonId": id,
    "title": "Lesson " + id,
    "summary": catalog['lessons'][id]["summary"]
  }
  return jsonify(overview)

@app.route('/api/lesson/content/<lid>/<sid>')
def api_lesson_content(lid, sid):
  sid = int(sid) - 1
  data = catalog['lessons'][lid]['content'][sid]
  content = {
    "lead": data['lead'],
    "example": data['example'],
    "explanation": data['explanation']
  }
  return jsonify(content);

@app.route('/api/quiz/overview/multiple/<id>')
def api_quiz_multi_overview(id):
  overview = {
    "quizId": id,
    "type": "multiple",
    "title": "Multiple Choice Quiz",
    "summary": catalog['quizzes']['multiple'][id]["summary"]
  }
  return jsonify(overview)

@app.route('/api/quiz/overview/write/<id>')
def api_quiz_write_overview(id):
  overview = {
    "quizId": id,
    "type": "write",
    "title": "Written Quiz",
    "summary": catalog['quizzes']['write'][id]["summary"]
  }
  return jsonify(overview)

@app.route('/api/quiz/content/multiple/<id>')
def api_quiz_multiple(id):
  content = catalog['quiz']['write'][str(id)]['content'][0]
  return jsonify(content)

@app.route('/api/quiz/content/write/<id>')
def api_quiz_write(id):
  content = catalog['quizzes']['write'][str(id)]['content'][0]
  return jsonify(content)

@app.route('/api/pinyin/<char>')
def api_pinyin(char):
  response = requests.get("https://glosbe.com/transliteration/api?from=Han&dest=Latin&text=" + char + "&format=json")
  data = response.json()
  return jsonify(data)

if __name__ == '__main__':
  app.run(host = '0.0.0.0', port = 8000)