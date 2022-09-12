from flask import Flask
import os
app = Flask(__name__)


@app.route("/")
def home():
    return "Hello, Flask!"


@app.route("/about")
def about():
    return "About page"
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
app = Flask(__name__)


@app.route('/')
def index():
   print('Request for index page received')
   return render_template('index.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/hello', methods=['POST'])
def hello():
   name = request.form.get('name')

   if name:
       print('Request for hello page received with name=%s' % name)
       return render_template('hello.html', name = name)
   else:
       print('Request for hello page received with no name or blank name -- redirecting')
       return redirect(url_for('index'))

@app.route('/ml', methods=['POST'])
def ml():

    try: 
        textinput = request.form.get('textinput')
        deployment = request.form.get('deployment')
        from ml import dummyep
        retstr = dummyep.ml_endpoint(textinput, deployment)
        print(retstr)
        return render_template('dummyep.html', result = retstr, deployment=deployment)
    except Exception as e:
        return str(e)
    # return "ml button clicked"

if __name__ == '__main__':
   app.run()