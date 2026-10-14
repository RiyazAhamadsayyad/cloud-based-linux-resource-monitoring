from flask import Flask, render_template
import psutil

app = Flask(__name__)

@app.route("/")
def home():
    cpu = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory().percent
    disk = psutil.disk_usage("/").percent

    if cpu > 80 or memory > 80:
        status = "HIGH LOAD - SCALE UP"
    elif cpu < 30:
        status = "LOW LOAD - SCALE DOWN"
    else:
        status = "NORMAL"

    return render_template(
        "index.html",
        cpu=cpu,
        memory=memory,
        disk=disk,
        status=status
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
