import os
import time
import json
import requests
import pandas as pd
from datetime import datetime
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from config import *

class SeattlePermitScraper:
    def __init__(self):
        self.session = requests.Session()
        self.google_creds = None
        self.sheets_service = None

    def setup_google_sheets(self):
        """Initialize Google Sheets API connection"""
        SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
        
        if os.path.exists('token.json'):
            self.google_creds = Credentials.from_authorized_user_file('token.json', SCOPES)
            
        if not self.google_creds or not self.google_creds.valid:
            if self.google_creds and self.google_creds.expired and self.google_creds.refresh_token:
                self.google_creds.refresh(Request())
            else:
                print("Opening browser for Google authorization...")
                flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
                self.google_creds = flow.run_local_server(port=0)
                print("Authorization complete!")
            with open('token.json', 'w') as token:
                token.write(self.google_creds.to_json())
                
        self.sheets_service = build('sheets', 'v4', credentials=self.google_creds)

    def write_startup_message(self):
        """Write a startup confirmation message to the Google Sheet"""
        if not self.sheets_service:
            self.setup_google_sheets()

        try:
            startup_message = [
                ["Seattle Permit Scraper Status"],
                [f"Scraper started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"],
                ["Status: Active"],
                ["Update frequency: Every 6 hours"],
                [""],  # Empty row
                ["Permit Data will appear below:"],
                [""]  # Empty row for spacing
            ]
            
            self.sheets_service.spreadsheets().values().update(
                spreadsheetId=os.getenv('SPREADSHEET_ID'),
                range=f'{WORKSHEET_NAME}!A1',
                valueInputOption='RAW',
                body={'values': startup_message}
            ).execute()
            
            print("Successfully wrote startup message to Google Sheets")
            return True
        except Exception as e:
            print(f"Error writing startup message: {e}")
            return False

    def fetch_permits(self, filters=None):
        """Fetch permit data from Seattle API"""
        params = filters or DEFAULT_FILTERS
        try:
            response = self.session.get(SEATTLE_API_BASE_URL, params=params)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error fetching permits: {e}")
            return []

    def process_permits(self, permits):
        """Process and filter permit data"""
        df = pd.DataFrame(permits)
        if df.empty:
            return df
        
        # Select only the fields we want
        df = df[PERMIT_FIELDS]
        
        # Add timestamp
        df['fetch_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        return df

    def update_google_sheet(self, df):
        """Update Google Sheet with new permit data"""
        if not self.sheets_service:
            self.setup_google_sheets()

        try:
            # Convert DataFrame to values
            values = [df.columns.tolist()] + df.values.tolist()

            # Update the sheet starting after the header section
            self.sheets_service.spreadsheets().values().update(
                spreadsheetId=os.getenv('SPREADSHEET_ID'),
                range=f'{WORKSHEET_NAME}!A8',  # Start after the header section
                valueInputOption='RAW',
                body={'values': values}
            ).execute()
            
            print(f"Successfully updated {len(df)} permits to Google Sheets")
            
        except Exception as e:
            print(f"Error updating Google Sheet: {e}")

    def run(self):
        """Main execution loop"""
        print("Starting Seattle Permit Scraper...")
        
        # Write startup message and verify Google Sheets connection
        if not self.write_startup_message():
            print("Failed to connect to Google Sheets. Please check your credentials and permissions.")
            return

        print("Successfully connected to Google Sheets!")
        
        while True:
            print(f"Fetching permits at {datetime.now()}")
            
            # Fetch and process permits
            permits = self.fetch_permits()
            if permits:
                df = self.process_permits(permits)
                if not df.empty:
                    self.update_google_sheet(df)
            
            # Wait for next update
            time.sleep(UPDATE_INTERVAL)

if __name__ == "__main__":
    scraper = SeattlePermitScraper()
    scraper.run() 