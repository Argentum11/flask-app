from flask import Flask, render_template

app = Flask(__name__)
app.config.from_object("config.DevelopmentConfig")

@app.route("/")
def index():
    return render_template("index.html", username="john")

if __name__ == "__main__":
    app.run(port=8081)