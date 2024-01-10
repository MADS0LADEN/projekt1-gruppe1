from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        ssid = request.form['ssid']
        password = request.form['password']
        email = request.form['email']
        # Her kan du gøre noget med de indtastede værdier, som f.eks. gemme dem i en database eller udføre en handling med dem
        return f'Du har indtastet SSID: {ssid}, password: {password}, email: {email}'

if __name__ == '__main__':
    app.run(debug=True)
