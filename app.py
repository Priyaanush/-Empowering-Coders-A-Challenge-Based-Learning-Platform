import time
import math
import numpy as np
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import csv
import re
import random
from flask import Flask,request,render_template,redirect,url_for,jsonify,flash
import sqlite3
import json
import random
import openpyxl
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from difflib import SequenceMatcher
nltk.download('punkt')
nltk.download('stopwords')

l=[]

app=Flask(__name__)
db="final1.db"
def create_table():
    conn=sqlite3.connect(db)
    cursor=conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS reg1 (name text, phone int, pass int,mark int)")
    conn.commit()
    conn.close()
create_table()


@app.route("/")
@app.route("/index0",methods=["GET","POST"])
def index0():
    return render_template("index0.html")
l1=[]
@app.route('/log',methods=["GET","POST"] )
def log():
    if request.method == 'POST':
         name=request.form['name']
         password=request.form['Password']   
         if name == 'admin' and password == 'admin':
             return render_template("question.html")
         else:
            return "password mismatch"
     
    return render_template('log.html')



@app.route('/question', methods=['GET', 'POST'])
def question():
    if request.method == 'POST':
        global language
        question = request.form['ques']
        answer = request.form['solve']
        language = request.form['language']
        tokens = word_tokenize(answer)
        stop_words = set(stopwords.words('english'))
        filtered_tokens = [word for word in tokens if word.lower() not in stop_words]
        orig_ques = question
        keywords = filtered_tokens
        if language == 'java':
            with open('java.csv', mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([orig_ques, keywords])
            try:
                with open('questions_and_answers_java.json', 'r') as json_file:
                    existing_data = json.load(json_file)
            except (FileNotFoundError, json.decoder.JSONDecodeError):
                existing_data = []
            question_number = len(existing_data) + 1

            data = {
                "question_number": question_number,
                "question": question,
                "answer": {
                    "code": answer,
                }
            }
            existing_data.append(data)
            with open('questions_and_answers_java.json', 'w') as json_file:
                json.dump(existing_data, json_file, indent=2)
            flash('Question successfully saved', 'success fully saved Question')
            #print("Question successfully saved")
            return redirect(url_for('question'))
        
        elif language == 'python':
            with open('python.csv', mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([orig_ques, keywords])
            try:
                with open('questions_and_answers_python.json', 'r') as json_file:
                    existing_data = json.load(json_file)
            except (FileNotFoundError, json.decoder.JSONDecodeError):
                existing_data = []
            question_number = len(existing_data) + 1

            data = {
                "question_number": question_number,
                "question": question,
                "answer": {
                    "code": answer,
                }
            }
            existing_data.append(data)
            with open('questions_and_answers_python.json', 'w') as json_file:
                json.dump(existing_data, json_file, indent=2)
            flash('Question successfully saved', 'success fully saved Question')
            #print("Question successfully saved")
            return redirect(url_for('question'))
        
        elif language == 'c':
            with open('c.csv', mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([orig_ques, keywords])
            try:
                with open('questions_and_answers_c.json', 'r') as json_file:
                    existing_data = json.load(json_file)
            except (FileNotFoundError, json.decoder.JSONDecodeError):
                existing_data = []
            question_number = len(existing_data) + 1

            data = {
                "question_number": question_number,
                "question": question,
                "answer": {
                    "code": answer,
                }
            }
            existing_data.append(data)
            with open('questions_and_answers_c.json', 'w') as json_file:
                json.dump(existing_data, json_file, indent=2)
            flash('Question successfully saved', 'success fully saved Question')
            #print("Question successfully saved")
            return redirect(url_for('question')) 
    return render_template('question.html')


@app.route("/index1",methods=["GET","POST"])
def index1():
    return render_template("index1.html")


@app.route("/register",methods=["GET","POST"])
def register():
        name=request.form['username']
        phone=request.form['ph']
        password=request.form['password']
        mark=0
        conn=sqlite3.connect(db)
        cursor=conn.cursor()
        cursor.execute("insert into reg1 (name,phone,pass,mark)values(?,?,?,?)",(name,phone,password,mark))
        conn.commit()
        return render_template("index1.html")
    
@app.route('/login',methods=["GET","POST"])
def login():
     name=request.form['name']
     l1.append(name)
     password=request.form['Password']
     conn=sqlite3.connect(db)
     cursor=conn.cursor()
     cursor.execute("select name , pass  from reg1 WHERE name = ? AND pass = ?", (name, password))
     data=cursor.fetchone()
     if data:
         return render_template("index.html")
     else:
        return "password mismatch"


def load_questions():
    with open('python.csv', 'r') as file:
        lines = file.readlines()
        first_column_content = [row.split(',')[0].strip(" '\"") for row in lines]
    return first_column_content

def load_questions1():
    with open('java.csv', 'r') as file:
        lines = file.readlines()
        first_column_content = [row.split(',')[0].strip(" '\"") for row in lines]
    return first_column_content


def load_questions2():
    with open('c.csv', 'r') as file:
        lines = file.readlines()
        first_column_content = [row.split(',')[0].strip(" '\"") for row in lines]
    return first_column_content



@app.route('/python', methods=['GET','POST'])
def python():
    questions=load_questions()
    l.append("python")
    #print("python")
    return render_template('python.html', question = questions)

@app.route('/java', methods=['GET','POST'])
def java():
     l.append("java")
     questions=load_questions1()
     return render_template('java.html', question = questions)
    
@app.route('/c', methods=['GET','POST'])
def c():
     l.append("c")
     questions=load_questions2()
     #print(questions)
     return render_template('c.html', question = questions)

    
def index1():
    if l[-1]=="python":
        with open('questions_and_answers_python.json', 'r') as file:
            data = json.load(file)
    elif l[-1]=="java":
        with open('questions_and_answers_java.json', 'r') as file:
            data = json.load(file)
            #print("java")
    elif l[-1]=="c":
        with open('questions_and_answers_c.json', 'r') as file:
            data = json.load(file)
            #print(data)
    return data

current_question_index = 0
@app.route('/generate_question')
def generate_question():
    global current_question_index
    data=index1()
    if current_question_index < len(data):
        current_question = data[current_question_index]['question']
        #print("python generate")
        question_number = data[current_question_index]['question_number']
        current_question_index += 1
        return jsonify({'question_number': question_number, 'question': current_question})
    else:
        return jsonify({'question_number': None, 'question': 'No more questions'})


@app.route('/generate_question1')
def generate_question1():
    global current_question_index
    data=index1()
    if current_question_index < len(data):
        current_question = data[current_question_index]['question']
        #print("python generate")
        question_number = data[current_question_index]['question_number']
        current_question_index += 1
        return jsonify({'question_number': question_number, 'question': current_question})
    else:
        return jsonify({'question_number': None, 'question': 'No more questions'})





@app.route('/generate_question2')
def generate_question2():
    global current_question_index
    data=index1()
    if current_question_index < len(data):
        current_question = data[current_question_index]['question']
        #print("c generate")
        question_number = data[current_question_index]['question_number']
        current_question_index += 1
        return jsonify({'question_number': question_number, 'question': current_question})
    else:
        return jsonify({'question_number': None, 'question': 'No more questions'})




@app.route('/store_question_answer', methods=['POST','GET'])
def store_question_answer():
    global row_counter  
    user_question = request.form.get('question')
    #print(user_question,"answer")
    question_number = request.form.get('question_number')
    #print(question_number,"question number")
    tokens = word_tokenize(user_question)
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [word for word in tokens if word.lower() not in stop_words]
    orig_ques=question
    keywords=filtered_tokens
    if l[-1]=="python":
        data = pd.read_csv("python.csv",header=None)
        value=int(question_number)-1
        value_row2_col2 = data.iloc[value,1]
        with open('python2.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([value_row2_col2,keywords])
    elif l[-1]=="java":
        data = pd.read_csv("java.csv",header=None)
        value=int(question_number)-1
        value_row2_col2 = data.iloc[value,1]
        with open('java2.csv', mode='w', newline='') as file:   
            writer = csv.writer(file)
            writer.writerow([value_row2_col2,keywords])
    elif l[-1]=="c":
        data = pd.read_csv("c.csv",header=None)
        value=int(question_number)-1
        value_row2_col2 = data.iloc[value,1]
        with open('c2.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([value_row2_col2,keywords])
    else:
        print("nothing")
    return "succues"


def checkmark():
        special_chars = re.compile(r'[^a-zA-Z0-9 ]+')
        if l[-1]=="python":
            file="python2.csv"
        elif l[-1]=="java":
            file="java2.csv"
        else:
            file="c2.csv"
        with open(file, newline='') as csvfile:
            reader = csv.reader(csvfile)
            data = [row[:2] for row in reader] 
        clean_data = [[special_chars.sub('', cell).lower() for cell in row] for row in data]
        total_ratio = 0.0
        for row in clean_data:
            ratio = SequenceMatcher(None, row[0], row[1]).ratio()
            total_ratio += ratio
        avg_ratio = total_ratio / len(clean_data)
        percent_match = round(avg_ratio * 100, 2)
        #print(percent_match)
        if percent_match>90:
            answer=1
            conn=sqlite3.connect(db)
            cursor=conn.cursor()
            name=l1[-1]
            cursor.execute("select mark from reg1 where name=?",(name,))
            data=cursor.fetchone()
            data1=data[0]
            mark=int(data1)+1
            #print(mark)
            conn=sqlite3.connect(db)
            cursor=conn.cursor()
            cursor.execute("UPDATE reg1 SET mark=? WHERE name=?", (mark, name))
            conn.commit()
        else:
            answer=0
        return answer
        

@app.route('/result', methods=['POST','GET'])
def result():
    mark=checkmark()
    return render_template("result.html",result=mark)



@app.route('/get_answer/<question_number>', methods=['GET'])
def get_answer(question_number):
    if l[-1] == "python":
        with open('questions_and_answers_python.json', 'r') as file:
            data = json.load(file)
    elif l[-1] == "java":
        with open('questions_and_answers_java.json', 'r') as file:
            data = json.load(file)
    elif l[-1] == "c":
        with open('questions_and_answers_c.json', 'r') as file:
            data = json.load(file)
    else:
        print("nothing")

    question_number = int(question_number)
    answer = data[question_number - 1]['answer']['code']
    
    return jsonify({'answer': answer})


@app.route('/admin', methods=['POST','GET'])
def admin():
            conn=sqlite3.connect(db)
            cursor=conn.cursor()
            cursor.execute("SELECT name, phone, mark FROM reg1")
            data=cursor.fetchall()
            return render_template('admin.html', data = data)

@app.route('/result2', methods=['POST','GET'])
def result2():
            conn=sqlite3.connect(db)
            cursor=conn.cursor()
            name=l1[-1]
            cursor.execute("SELECT name, phone, mark FROM reg1 where name=?",(name,))
            data=cursor.fetchall()
            return render_template('admin.html', data = data)                

                    
if __name__=="__main__":
    app.secret_key = "13243566@#$^%dgftrd45645#@$%^"
    app.run(port=450,debug=False)
