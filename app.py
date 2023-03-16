from flask import Flask, render_template, request, redirect, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = '<78412310>'
toolbar = DebugToolbarExtension(app)

SURVEY = satisfaction_survey

@app.route('/')
def landing_page():
  return render_template('start.html', survey=SURVEY)

@app.route('/set-session', methods=['POST'])
def set_responses():
  session['responses'] = []
  return redirect('/questions/0')

@app.route('/questions/<int:q>')
def survey(q):
  responses = session.get('responses')
  if len(responses) == len(SURVEY.questions):
    return redirect('/thanks')
  elif q != len(responses):
    q = len(responses)
  return render_template('survey.html', survey=SURVEY, q=q)

@app.route('/next-question/<int:q>', methods=['POST'])
def next_question(q):
  responses = session.get('responses')
  for choice in SURVEY.questions[q].choices:
    answer = request.form.get(choice)
    if answer:
      responses.append(choice)
  
  session['responses'] = responses
  
  if len(responses) < len(SURVEY.questions):
    return redirect(f'/questions/{q + 1}')
  else:
    return redirect('/thanks')

@app.route('/thanks')
def answers():
  answers = session.get('responses')
  return render_template('thanks.html', answers=answers, questions=SURVEY.questions)

