from flask import Flask, render_template, request

app = Flask(__name__, static_folder='static')

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/food')
def food():
    return render_template('food.html')

if __name__ == "__main__":
    app.run(debug=True)
