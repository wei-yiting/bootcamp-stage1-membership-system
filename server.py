from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__, static_folder="public", static_url_path="/")
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


@app.route('/')
def index():
    session["status"] = "未登入"
    return render_template('index.html')


@app.route('/signin', methods=["POST"])
def signin():
    username = request.form["username"]
    password = request.form["password"]
    if username == 'test' and password == 'test':
        session["status"] = "已登入"
        return redirect(url_for('member'))
    return redirect(url_for('error'))


@app.route('/error')
def error():
    return render_template('error.html')


@app.route('/member')
def member():
    if session["status"] == "已登入":
        return render_template('member.html')
    elif session["status"] == "未登入":
        return redirect(url_for('index'))


@app.route('/signout', methods=['GET'])
def signout():
    session["status"] = "未登入"
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(port=3000, debug=True)
