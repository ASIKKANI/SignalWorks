# SignalWorks Constants & Configuration

CITIES = ["Mumbai", "Delhi", "Bangalore", "Chennai", "Hyderabad", "Kolkata"]

import os
from dotenv import load_dotenv
load_dotenv()

# API Keys (Loaded from environment variables for security)
OPENWEATHER_API_KEY = os.environ.get("OPENWEATHER_API_KEY", "")
GOOGLE_MAPS_API_KEY = os.environ.get("GOOGLE_MAPS_API_KEY", "")

# AWS/Twilio Config
DATA_LAKE_BUCKET = "signalworks-data-lake"
BEDROCK_MODEL_ID = "apac.anthropic.claude-3-5-sonnet-20241022-v2:0"
TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID", "")
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN", "")
TWILIO_PHONE_NUMBER = os.environ.get("TWILIO_PHONE_NUMBER", "")

# Languages
SUPPORTED_LANGUAGES = {
    "Hindi": "hi",
    "Tamil": "ta",
    "Telugu": "te",
    "Kannada": "kn",
    "English": "en"
}

# Mandi Data (Agmarknet)
AGMARKNET_URL = "https://agmarknet.gov.in/SearchReports/SearchReport.aspx?Report_Name=DailyReportCust&State_Code=MH&District_Code=0&Market_Code=0&Arrival_Date={date}&Arrival_Date_To={date}&Commodity_Code=0"
