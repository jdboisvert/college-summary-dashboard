from flask import Flask, render_template

app = Flask(__name__, static_url_path='/static')


@app.route('/about', methods=['GET'])
def about():
    return render_template("about.html")


@app.route('/', methods=['GET'])
def dashboard():
    return render_template('dashboard.html')


if __name__ == '__main__':
    app.run(debug=True)