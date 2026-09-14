from flask import Flask, render_template, request
from Users import UserModel

app = Flask(__name__)
app.config.from_object("config.DevelopmentConfig")
userModel = UserModel("users.csv")

@app.route("/")
def bmi_form():
    return render_template("bmi_form.html")

@app.route("/bmi", methods=["POST"])
def bmi_result():
    height_cm = request.form["height"]
    weight_kg = request.form["weight"]

    try:
        height_m = float(height_cm) / 100
        weight = float(weight_kg)
        if height_m <= 0 or weight <= 0:
            raise ValueError
    except ValueError:
        return render_template(
            "bmi_error.html", error="Enter positive numbers for height and weight."
        )

    bmi = round(weight / (height_m ** 2), 1)
    return render_template("bmi_result.html", bmi=bmi, height=height_cm, weight=weight_kg)


@app.route("/users")
def users():
    return render_template("users.html", users=userModel.get_users())


if __name__ == "__main__":
    app.run(port=8081)