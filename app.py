from flask import Flask, render_template
from ip_info import IPInfo

app = Flask(__name__)


@app.route("/")
def home():

    info = IPInfo()

    info.ipv4 = info.get_ip("IPv4")
    info.ipv6 = info.get_ip("IPv6")

    success = info.get_details()

    return render_template(
        "index.html",
        info=info,
        success=success
    )


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
