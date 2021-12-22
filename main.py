from flask import Flask, render_template, request, redirect, abort, flash, url_for
from questions import get_question, get_answer
from utils import Email, is_human
import os

app = Flask(__name__)
app.secret_key = os.environ['SECRET_KEY']


@app.route('/')
def index():
    return render_template('home.html')


@app.route('/info')
def info():
    return render_template('info.html')


@app.route('/suggest')
def suggest():
    return render_template('suggest.html')


@app.route('/suggestion', methods=['GET', 'POST'])
def suggestion():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        question = request.form['question']
        answer = request.form['answer']
        type = request.form['type']
        topic = request.form['topic']
        sensible = request.form['sensible']
        accurate = request.form['accurate']
        captcha_response = request.form['g-recaptcha-response']

        if not is_human(captcha_response):
            print('Bot attempt!')
            flash(
                'Please complete the reCAPTCHA to confirm that you\'re not a robot',
                category='error')
            return redirect(url_for('suggest'))

        content = f'Name: {name}\nEmail: {email}\nQuestion: {question}\nAnswer: {answer}\nType: {type}\nTopic: {topic}'

        if sensible == 'Agreed' and accurate == 'Agreed':
            email = Email()
            sent = email.sendEmail(content)

            if sent:
                flash('Suggestion submitted successfully', category='success')
            else:
                flash('Error submitting suggestion. Please try again later',
                      category='error')

        return redirect(url_for('suggest'))


@app.route('/question')
def random_question():
    return redirect('/question/random')


@app.route('/question/<topic>')
def question(topic: str):
    if topic.lower() == 'random':
        type, topic, question, id, option1, option2, option3, ok = get_question(
        )
    else:
        type, topic, question, id, option1, option2, option3, ok = get_question(
            topic.lower())

    if ok:

        return render_template('question.html',
                               type=type,
                               topic=topic,
                               question=question,
                               option1=option1,
                               option2=option2,
                               option3=option3,
                               id=id)

    else:
        abort(404)


@app.route('/result', methods=['POST'])
def check_question():
    if request.method == 'POST':
        question = request.form['question']
        user_answer = request.form['user_answer']
        id = request.form['id']
        answer = get_answer(int(id))
        if user_answer.lower() == answer.lower():
            return render_template('result.html',
                                   question=question,
                                   user_answer=user_answer,
                                   answer=answer,
                                   correct=True)
        else:
            return render_template('result.html',
                                   question=question,
                                   user_answer=user_answer,
                                   answer=answer,
                                   correct=False)


@app.errorhandler(404)
def not_found(e):
    return render_template('404.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
