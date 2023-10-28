"""entry of api"""
from api.v1.views import app_views


@app_views.route("/status")
def get_status():
    """get status"""
    return {"status": "OK"}
