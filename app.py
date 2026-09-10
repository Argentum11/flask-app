from flask import Flask, render_template

app = Flask(__name__)
app.config.from_object("config.DevelopmentConfig")

@app.route("/")
def index():
    return render_template("index.html", username="john")


@app.route("/users")
def users():
    users = [
        {"username": "Jacky",
            "age": 30.0},
        {"username": "Andy",
         "age": 18}
    ]
    return render_template("users.html", users=users)


if __name__ == "__main__":
    app.run(port=8081)