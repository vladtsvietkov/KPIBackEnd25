from backend import app

@app.route("/healthcheck")
def healthcheck():
    return {"status": "OK", "message": "Backend is functional"}