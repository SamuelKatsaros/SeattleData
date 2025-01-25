# Seattle API Configuration
SEATTLE_API_BASE_URL = "https://data.seattle.gov/resource/76t5-zqzr.json"

# Fields to fetch from the API
PERMIT_FIELDS = [
    "permitnum",
    "permitclass",
    "permitclassmapped",
    "permittypedesc",
    "description",
    "statuscurrent",
    "originaladdress1",
    "originalcity",
    "originalstate",
    "originalzip",
    "link"
]

# Google Sheets Configuration
SPREADSHEET_NAME = "Seattle Construction Permits"
WORKSHEET_NAME = "Active Permits"

# Default filters
DEFAULT_FILTERS = {
    "permitclass": "Commercial",  # Focus on commercial permits
    "statuscurrent": "Application Accepted"  # Only active permits
}

# Update frequency in seconds (default: every 6 hours)
UPDATE_INTERVAL = 21600 