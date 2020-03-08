from flask import Flask, request, render_template
from parser import parse_file

app = Flask(__name__)


def get_data(f):
    conversation = parse_file(f)
    data = {
        "name": conversation.name,
        "message_counts": conversation.message_counts,
        "message_rate_day": conversation.message_rate("day"),
        "message_rate_hour": conversation.message_rate("hour"),
    }

    time_composition = [
        conversation.time_composition(visualize=False)[x] for x in range(24)
    ]

    data["time_comp"] = time_composition
    return data


@app.route("/")
def hello():
    return render_template("index.html", error=False)


@app.route("/submit", methods=["POST"])
def get_file():
    f = request.files["text-file"]
    try:
        data = get_data(f)
        return render_template("analysis.html", data=data)
    except Exception as e:
        err = str(e)
        return render_template("index.html", error=err)


if __name__ == "__main__":
    app.run(debug=True)
