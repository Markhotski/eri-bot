import os
from dotenv import load_dotenv

load_dotenv()

# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

# API Configuration
API_URL = os.getenv('API_URL', 'https://eri2.nca.by/api/guest/abandonedObject/search')
VIEW_URL_BASE = os.getenv('VIEW_URL_BASE', 'https://eri2.nca.by/api/guest/abandonedObject')
CHECK_INTERVAL_HOURS = int(os.getenv('CHECK_INTERVAL_HOURS', 1))

# Proxy Configuration (optional)
HTTP_PROXY = os.getenv('HTTP_PROXY')
HTTPS_PROXY = os.getenv('HTTPS_PROXY')

# Search payload for the API with specific filters
# Searches for objects in specific region (ateId: 19824) with other criteria
# Returns empty list [] if no objects match the search criteria
SEARCH_PAYLOAD = {
    "pageSize": 10,
    "pageNumber": 0,
    "sortBy": 1,
    "sortDesc": True,
    "abandonedObjectId": None,
    "fromInspectionDate": None,
    "toInspectionDate": None,
    "fromEventDate": None,
    "toEventDate": None,
    "abandonedObjectTypeId": 1,
    "stateTypeId": None,
    "stateGroupId": None,
    "stateSearchCategoryId": 2,
    "streetId": None,
    "ateId": 19824,
    "oneBasePrice": True,
    "emergency": False,
    "destroyed": False,
    "fromDeterioration": None,
    "toDeterioration": None,
    "fromMoneyAmount": None,
    "toMoneyAmount": None
}

# Data persistence
DATA_FILE = 'last_check_data.json'
