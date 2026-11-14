from flask import Flask, render_template, request, g
from v1 import v1_bp

import uuid
import time

app = Flask(__name__)
app.config.from_object("config.DevelopmentConfig")
app.register_blueprint(v1_bp, url_prefix="/v1")


@app.before_request
def preprocess():
    g.uuid = uuid.uuid4()
    g.conn = {"is_connected": True}
    g.start = time.perf_counter()


@app.after_request
def postprocess(response):
    duration_ms = (time.perf_counter() - g.start) * 1000
    app.logger.info(
        "%s %s %s -> %s (%s bytes) in %.2f ms",
        g.uuid, request.method, request.path,
        response.status_code, response.content_length, duration_ms
    )
    response.headers["X-Request-ID"] = str(g.uuid)
    return response


@app.teardown_request
def cleanup(exception):
    g.conn["is_connected"] = False
    app.logger.info(g.conn)


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


if __name__ == "__main__":
    # check for all routes
    # print(app.url_map)
    app.run(port=8081)
