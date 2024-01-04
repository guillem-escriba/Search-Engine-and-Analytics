from myapp.data_collection.data_models import Session_Data, Click_Data, Request_Data

class DataStorage:
    def __init__(self):
        self.sessions = {}
        self.clicks = {}
        self.requests = {}

    def add_session(self, session):
        self.sessions[session.session_id] = session

    def add_click(self, click):
        self.clicks[click.click_id] = click

    def add_request(self, request):
        self.requests[request.request_id] = request
