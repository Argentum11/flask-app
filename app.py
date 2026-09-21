from flask import Flask, render_template, request, jsonify
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
    return jsonify(userModel.get_users(user_id=None))


@app.route("/users/<int:user_id>")
def user(user_id):
    user = userModel.get_users(user_id=user_id)
    if user is None:
        return jsonify({"error": "User not found!"}), 404
    return jsonify(user)


@app.route("/users", methods=["POST"])
def add_user():
    new_user = userModel.add_user(
        username=request.json["username"], age=request.json["age"])
    response = jsonify(new_user)
    response.headers["location"] = f"/users/{new_user["user_id"]}"
    return response, 201


@app.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    if userModel.delete_user(user_id=user_id):
        return "", 204
    else:
        return jsonify({"message": "User not found"}), 404


@app.route("/users/<int:user_id>", methods=["PUT", "PATCH"])
def update_user(user_id):
    new_username = request.json["username"] if "username" in request.json else None
    new_age = request.json["age"] if "age" in request.json else None
    updated_user = userModel.update_user(
        user_id=user_id, new_username=new_username, new_age=new_age)
    if updated_user is None:
        return jsonify({"error": "User not found!"}), 404
    else:
        return jsonify(updated_user)


if __name__ == "__main__":
    app.run(port=8081)
