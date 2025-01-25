# Seattle Permit Scraper

A scalable Python application that fetches construction permit data from Seattle's Open Data API and automatically syncs it to Google Sheets. Built for security companies looking to identify new construction opportunities.

## Features

- Automated fetching of construction permit data from Seattle Gov API
- Integration with Google Sheets for easy data access and sharing
- Configurable filters for permit types and status
- Timestamp tracking for all fetched permits
- Extensible architecture for future features (email notifications, automated outreach, etc.)

## Setup

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up Google Sheets API:
   - Go to Google Cloud Console
   - Create a new project
   - Enable Google Sheets API
   - Create credentials (OAuth 2.0 Client ID)
   - Download the credentials and save as `credentials.json` in the project root

4. Create a `.env` file with:
   ```
   SPREADSHEET_ID=your_google_sheet_id
   ```

## Usage

Run the scraper:
```bash
python main.py
```

The script will:
1. Fetch permit data every 6 hours (configurable in config.py)
2. Process and filter the data based on configured criteria
3. Update the specified Google Sheet with new permits

## Configuration

Edit `config.py` to customize:
- API endpoint
- Fields to fetch
- Update frequency
- Default filters
- Google Sheets settings

## Future Extensions

The codebase is designed to be easily extended with:
- Email notifications for new permits
- Automated email outreach to permit holders
- Additional data sources
- Custom filtering and processing logic
- Different output formats (CSV, database, etc.)

## Requirements

- Python 3.8+
- Google account with Sheets API access
- Internet connection for API access # SeattleData
