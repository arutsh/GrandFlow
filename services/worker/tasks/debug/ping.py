from celery_app import app


@app.task(name="tasks.debug.ping", queue="ai")
def ping():
    return {"pong": True}
