import threading

from flask import Flask, render_template, redirect, request, url_for, flash

from file_manager import ensure_log_exists, read_file
from requester import (
    main_func,
    periodic_reading,
    reading_at,
    return_reading,
    return_by_download,
    return_by_upload,
    return_all,
    scheduler,
)
from WiGraph.plot import graph_download, graph_upload

# ── App init ─────────────────────────────────────────────────────────────────

ensure_log_exists()   # create Logs/log.json if it doesn't exist — once, here only

app = Flask(__name__)
app.secret_key = "wispeed-change-me-in-production"   # needed for flash messages


# ── Routes ───────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    try:
        data = read_file()
    except (FileNotFoundError, ValueError) as e:
        print(f"[app] Could not read log: {e}")
        data = []
    return render_template("index.html", data=data)


@app.route("/run_main", methods=["POST"])
def run_main():
    """Run a single speed test directly — no subprocess."""
    success = main_func()
    if success:
        flash("Speed test complete!", "success")
    else:
        flash("Speed test failed — check the console for details.", "error")
    return redirect(url_for("index"))


@app.route("/run_periodical", methods=["POST"])
def run_periodical():
    """
    Start periodic readings in a background thread so the server stays responsive.
    The browser redirects immediately; readings happen in the background.
    """
    try:
        frequency       = float(request.form["frequency"])
        max_occurrences = int(request.form["occurrences"])
    except (KeyError, ValueError) as e:
        flash(f"Invalid input: {e}", "error")
        return redirect(url_for("index"))

    if frequency <= 0 or max_occurrences <= 0:
        flash("Frequency and occurrences must be greater than zero.", "error")
        return redirect(url_for("index"))

    def run_in_background():
        messages = periodic_reading(frequency, max_occurrences)
        print(f"[app] Periodic run complete: {messages}")

    thread = threading.Thread(target=run_in_background, daemon=True)
    thread.start()

    flash(f"Started {max_occurrences} reading(s) every {frequency} min in the background.", "info")
    return redirect(url_for("index"))


@app.route("/return_dated", methods=["POST"])
def return_dated():
    try:
        date = request.form["date"]
        readings = return_reading(date)
        return render_template("index.html", data=readings)
    except (KeyError, ValueError) as e:
        flash(f"Invalid date input: {e}", "error")
    return redirect(url_for("index"))


@app.route("/return_all_readings", methods=["POST"])
def return_all_readings():
    try:
        readings = return_all()
        return render_template("index.html", data=readings)
    except Exception as e:
        flash(f"Could not load readings: {e}", "error")
    return redirect(url_for("index"))


@app.route("/view_by_download", methods=["POST"])
def view_by_download():
    try:
        readings = return_by_download()
        return render_template("index.html", data=readings)
    except Exception as e:
        flash(f"Could not sort readings: {e}", "error")
    return redirect(url_for("index"))


@app.route("/view_by_upload", methods=["POST"])
def view_by_upload():
    try:
        readings = return_by_upload()
        return render_template("index.html", data=readings)
    except Exception as e:
        flash(f"Could not sort readings: {e}", "error")
    return redirect(url_for("index"))


@app.route("/run_dated", methods=["POST"])
def run_dated():
    try:
        time_str = request.form["time"]
        scheduled = reading_at(time_str)
        if scheduled:
            flash(f"Test scheduled for {time_str}.", "success")
        else:
            flash("Could not schedule — time may be invalid or already passed.", "error")
    except (KeyError, ValueError) as e:
        flash(f"Invalid time input: {e}", "error")
    return redirect(url_for("index"))


@app.route("/to_graph_index", methods=["GET"])
def to_graph_index():
    download_graph = graph_download()
    upload_graph   = graph_upload()
    return render_template(
        "graph_index.html",
        plot_download=download_graph,
        plot_upload=upload_graph,
    )


# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    app.run(debug=True)
