from microdot import Microdot

app = Microdot()

@app.route('/')
def index(request):
    return app.send_static_file('index.html')

@app.route('/submit', methods=['POST'])
def submit(request):
    ssid = request.form.get('ssid')
    password = request.form.get('password')
    email = request.form.get('email')

    # Gør noget med de indtastede værdier, f.eks. gem i en database

    return f'Du har indtastet SSID: {ssid}, password: {password}, email: {email}'

if __name__ == '__main__':
    app.run(debug=True)
