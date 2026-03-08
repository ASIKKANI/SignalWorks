import json
import os
import boto3
import logging
from datetime import datetime
from twilio.rest import Client
from shared.constants import DATA_LAKE_BUCKET, SUPPORTED_LANGUAGES, TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Initialize Twilio Client
twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

translate = boto3.client('translate', region_name='ap-south-2')
s3 = boto3.client('s3')

# Mock Vendor Data
MOCK_VENDORS = [
    {"id": "V001", "name": "Bharani", "city": "Chennai", "area": "Kelambakkam", "phone": "+918681980569", "lang": "English"}
]

def translate_message(text, target_lang_name):
    """
    Translates text to the target language using Amazon Translate.
    """
    target_code = SUPPORTED_LANGUAGES.get(target_lang_name, 'en')
    if target_code == 'en':
        return text

    try:
        if os.environ.get('AWS_EXECUTION_ENV'):
            response = translate.translate_text(
                Text=text,
                SourceLanguageCode="en",
                TargetLanguageCode=target_code
            )
            return response['TranslatedText']
        else:
            # Mock translation for local testing
            return f"[{target_lang_name.upper()}] {text}"
    except Exception as e:
        logger.error(f"Translation failed: {str(e)}")
        return text

def send_sms(phone, message):
    """
    Sends SMS using Twilio.
    """
    try:
        # Use Twilio to send the message regardless of the environment now that we have keys!
        message_res = twilio_client.messages.create(
            body=message,
            from_=TWILIO_PHONE_NUMBER,
            to=phone
        )
        logger.info(f"Twilio SMS sent successfully. SID: {message_res.sid}")
        return {"Status": "Success", "SID": message_res.sid}
    except Exception as e:
        logger.error(f"Twilio failed: {str(e)}")
        return None

def lambda_handler(event, context):
    """
    Deliver Phase Lambda (6:00 AM).
    Fetches insights, translates them, and sends to vendors.
    """
    try:
        date_str = datetime.now().strftime('%Y-%m-%d')
        
        # 1. Load Insights
        if os.environ.get('AWS_EXECUTION_ENV'):
            file_key = f"analyze/processed/{date_str}/vendor_insights.json"
            obj = s3.get_object(Bucket=DATA_LAKE_BUCKET, Key=file_key)
            insights_data = json.loads(obj['Body'].read())
        else:
            local_path = f"data/lake/vendor_insights_{date_str}.json"
            if not os.path.exists(local_path):
                return {"statusCode": 404, "body": "Insights data not found"}
            with open(local_path, 'r') as f:
                insights_data = json.load(f)

        # Map insights by city for easy lookup
        city_insights = {item['city']: item for item in insights_data['insights']}

        # 2. Iterate through vendors and deliver
        # Allow a custom phone number to be injected via the event (e.g. from the dashboard demo)
        custom_phone = event.get('custom_phone') if event else None
        vendors = [dict(v, phone=custom_phone) for v in MOCK_VENDORS] if custom_phone else MOCK_VENDORS

        delivery_results = []
        for vendor in vendors:
            city = vendor['city']
            insight = city_insights.get(city)
            
            if insight:
                # Construct base message
                base_message = f"SignalWorks: {insight['summary']} {insight['fair_price_advice']}. Golden Hour: {insight['golden_hour']}."
                
                # Translate
                translated_msg = translate_message(base_message, vendor['lang'])
                
                # Send SMS
                status = send_sms(vendor['phone'], translated_msg)
                
                delivery_results.append({
                    "vendor_id": vendor['id'],
                    "city": city,
                    "status": "Sent" if status else "Failed"
                })

        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "Deliver phase completed successfully",
                "total_sent": len(delivery_results),
                "results": delivery_results
            })
        }

    except Exception as e:
        logger.error(f"Error in Deliver phase: {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
