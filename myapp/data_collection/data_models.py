import geoip2.database

def get_location(ip_address):
    try:
        with geoip2.database.Reader('ip_db\GeoLite2-City_20231205\GeoLite2-City.mmdb') as reader:
            response = reader.city(ip_address)
            city = response.city.name
            country = response.country.name
            return city, country
    except geoip2.errors.AddressNotFoundError:
        return "Private IP", "Location not Found"

def format_user_agent(user_agent_dict):
    platform = user_agent_dict.get('platform', {}).get('name', 'Unknown Platform')
    os = user_agent_dict.get('os', {}).get('name', 'Unknown OS') + " " + user_agent_dict.get('os', {}).get('version', '')
    browser = user_agent_dict.get('browser', {}).get('name', 'Unknown Browser') + " " + user_agent_dict.get('browser', {}).get('version', '')
    is_bot = "Yes" if user_agent_dict.get('bot', False) else "No"
    return f"OS: {os} (Platform: {platform}) Browser: {browser} Bot: {is_bot}"


class Session_Data:
    def __init__(self, session_id, user_ip, start_time, end_time=None, user_agent=None):
        self.session_id = session_id
        self.user_ip = user_ip
        self.location = get_location(str(user_ip))
        self.start_time = start_time
        self.end_time = end_time
        self.user_agent = user_agent

class Click_Data:
    def __init__(self, click_id, session_id, document_id, timestamp, query, rank):
        self.click_id = click_id
        self.session_id = session_id
        self.document_id = document_id
        self.timestamp = timestamp
        self.query = query
        self.rank = rank

class Request_Data:
    def __init__(self, request_id, session_id, query, timestamp):
        self.request_id = request_id
        self.session_id = session_id
        self.query = query
        self.timestamp = timestamp