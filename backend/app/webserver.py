from flask import Flask, request
from flask import render_template

app = Flask(__name__)

@app.route("/auth", methods=['POST'])
def get_privkey():
	print(request.form)
	print(request.form.get("privkey"))
	return "REPLY"
@app.route("/")
def hello():
	message = "Hello, world!"
	return render_template("index.html", message=message)

if __name__ == "__main__":
	app.run(debug=True, host='0.0.0.0', port=5000)
