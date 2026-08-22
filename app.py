from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/activity')
def activity():
    return render_template('activity.html')

@app.route('/catalog')
def catalog():
    return render_template('catalog.html')

if __name__ == '__main__':
    app.run(debug=True)
