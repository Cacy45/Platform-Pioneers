from flask import Flask, render_template, url_for


app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/student_login')
def student_login():
    return render_template('student_login.html')

@app.route('/student_dashboard')
def student_dashboard():
    return render_template('student_dashboard.html')



if __name__ == '__main__':
    app.run(debug=True)