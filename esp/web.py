import os

from microdot import Microdot

app = Microdot()


@app.route("/")
def index(request):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    index_path = os.path.join(dir_path, "index.html")
    with open(index_path, "r") as f:
        html_content = f.read()
    return html_content, {"Content-Type": "text/html"}


@app.route("/submit", methods=["POST"])
def submit(request):
    ssid = request.form.get("ssid")
    password = request.form.get("password")
    email = request.form.get("email")

    print(ssid, password, email)


if __name__ == "__main__":
    app.run(debug=False)
