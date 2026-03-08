import streamlit as st
import json
import os
import glob
import boto3
from dotenv import load_dotenv
load_dotenv()
from datetime import datetime

st.set_page_config(
    page_title="SignalWorks — AI Pipeline",
    page_icon="📡",
    layout="wide"
)

# ── Session State ──────────────────────────────────────────
defaults = {
    'step1_done': False, 'step1_output': '',
    'step2_done': False, 'step2_output': '',
    'step3_done': False, 'step3_output': '',
    'step4_done': False, 'step4_output': '',
    'sms_text': ''
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

def badge(done):
    return "✅ Complete" if done else "⏳ Pending"

def load_json(local_path, s3_key):
    """Reads JSON from S3 if in AWS mode, otherwise from local file."""
    if os.environ.get('AWS_EXECUTION_ENV'):
        try:
            s3 = boto3.client('s3')
            obj = s3.get_object(Bucket='signalworks-data-lake', Key=s3_key)
            return json.loads(obj['Body'].read())
        except Exception:
            return None
    else:
        if os.path.exists(local_path):
            with open(local_path) as f:
                return json.load(f)
        return None

# ── Header ─────────────────────────────────────────────────
st.markdown("# 📡 SignalWorks")
st.markdown("**AI-Powered Early Morning SMS Intelligence for Bharat's Street Vendors**")

col_sub, col_reset = st.columns([5, 1])
with col_sub:
    st.caption("EventBridge triggers this pipeline at 5:00 AM daily. Each step runs as an independent AWS Lambda function.")
with col_reset:
    if st.button("🔄 Reset Pipeline", use_container_width=True):
        for f in glob.glob("data/lake/*.json"):
            os.remove(f)
        for k in defaults:
            st.session_state[k] = defaults[k]
        st.rerun()

st.markdown("---")

# ══════════════════════════════════════════════════════════
# STEP 1 — INGEST
# ══════════════════════════════════════════════════════════
st.markdown("## Step 1 — 🌦️ Data Ingest")

left, right = st.columns([1, 2])

with left:
    st.markdown("Fetches live weather, Mandi commodity prices, traffic congestion and city events for 6 Indian cities.")
    st.markdown("")
    st.markdown("**AWS Services**")
    st.markdown("""
- 🟠 **Amazon S3** — stores raw data to the Data Lake
- 🌐 OpenWeatherMap API — live weather
- 🌐 Agmarknet — Mandi commodity prices
- 🌐 Google Maps — traffic congestion
    """)
    st.markdown(f"**Status:** {badge(st.session_state.step1_done)}")
    if st.button("▶  Run Ingest Lambda", use_container_width=True, type="primary", key="btn1"):
        with st.spinner("Lambda running — fetching live data..."):
            from functions.ingest.handler import lambda_handler as ingest_handler
            result = ingest_handler({}, None)
            body = json.loads(result['body'])
            if result['statusCode'] == 200:
                st.session_state.step1_done = True
                st.session_state.step1_output = (
                    f"Status: {result['statusCode']} OK\n"
                    f"Message: {body['message']}\n"
                    f"S3 Key: ingest/raw/{datetime.now().strftime('%Y-%m-%d')}/daily_ingest.json"
                )
            else:
                st.session_state.step1_output = f"ERROR: {body.get('error', 'Unknown')}"
        st.rerun()

with right:
    if st.session_state.step1_output:
        st.markdown("**Lambda Output**")
        st.code(st.session_state.step1_output, language="bash")

    if st.session_state.step1_done:
        date_str = datetime.now().strftime('%Y-%m-%d')
        data = load_json(
            f"data/lake/daily_ingest_{date_str}.json",
            f"ingest/raw/{date_str}/daily_ingest.json"
        )
        if data:
            cities = [d['city'] for d in data['data']]
            st.success(f"Data Lake  ·  {len(cities)} cities ingested: {', '.join(cities)}")
            for city_data in data['data'][:3]:
                w = city_data.get('weather') or {}
                if 'temp' in w:
                    st.info(f"🌡️ {city_data['city']}: {w['temp']}°C — {w.get('description', 'N/A')}")

st.markdown("---")

# ══════════════════════════════════════════════════════════
# STEP 2 — PREDICT
# ══════════════════════════════════════════════════════════
st.markdown("## Step 2 — 💰 Price Prediction")

left, right = st.columns([1, 2])

with left:
    st.markdown("Calculates fair retail prices for each commodity using the SageMaker ML model. Falls back to rule-based math if the endpoint is unavailable.")
    st.markdown("")
    st.markdown("**AWS Services**")
    st.markdown("""
- 🟠 **Amazon SageMaker** — ML price prediction model
- 🟠 **Amazon S3** — reads ingest data, writes predictions
    """)
    st.markdown(f"**Status:** {badge(st.session_state.step2_done)}")
    disabled = not st.session_state.step1_done
    if st.button("▶  Run Predict Lambda", use_container_width=True, type="primary", key="btn2", disabled=disabled):
        with st.spinner("Lambda running — SageMaker calculating fair prices..."):
            from functions.predict.handler import lambda_handler as predict_handler
            result = predict_handler({}, None)
            body = json.loads(result['body'])
            if result['statusCode'] == 200:
                st.session_state.step2_done = True
                st.session_state.step2_output = (
                    f"Status: {result['statusCode']} OK\n"
                    f"Message: {body['message']}\n"
                    f"Cities Processed: {body['cities_processed']}\n"
                    f"S3 Key: predict/forecasts/{datetime.now().strftime('%Y-%m-%d')}/price_predictions.json"
                )
            else:
                st.session_state.step2_output = f"ERROR: {body.get('error', 'Unknown')}"
        st.rerun()
    if disabled:
        st.caption("⚠️ Complete Step 1 first")

with right:
    if st.session_state.step2_output:
        st.markdown("**Lambda Output**")
        st.code(st.session_state.step2_output, language="bash")

    if st.session_state.step2_done:
        date_str = datetime.now().strftime('%Y-%m-%d')
        data = load_json(
            f"data/lake/price_predictions_{date_str}.json",
            f"predict/forecasts/{date_str}/price_predictions.json"
        )
        if data:
            any_preds = [c for c in data['predictions'] if c.get('commodities')]
            if any_preds:
                for city_pred in any_preds[:2]:
                    c = city_pred['commodities'][0]
                    st.info(f"📈 {city_pred['city']}: {c['name']} — Fair Price ₹{c['fair_retail_price_today']}/kg  ·  Trend: {c['trend']}")
            else:
                st.info("📊 Prices calculated via SageMaker rule-based fallback (no Mandi data was available from Agmarknet today)")

st.markdown("---")

# ══════════════════════════════════════════════════════════
# STEP 3 — ANALYZE
# ══════════════════════════════════════════════════════════
st.markdown("## Step 3 — 🧠 AI Analysis")

left, right = st.columns([1, 2])

with left:
    st.markdown("Amazon Bedrock invokes Claude 3.5 Sonnet to synthesize weather, prices and events into a single personalized insight per vendor.")
    st.markdown("")
    st.markdown("**AWS Services**")
    st.markdown("""
- 🟣 **Amazon Bedrock** — Claude 3.5 Sonnet (Generative AI)
- 🟠 **Amazon S3** — reads predictions, writes vendor insights
    """)
    st.markdown(f"**Status:** {badge(st.session_state.step3_done)}")
    disabled = not st.session_state.step2_done
    if st.button("▶  Run Analyze Lambda", use_container_width=True, type="primary", key="btn3", disabled=disabled):
        with st.spinner("Lambda running — Bedrock (Claude 3.5 Sonnet) generating insights..."):
            from functions.analyze.handler import lambda_handler as analyze_handler
            result = analyze_handler({}, None)
            body = json.loads(result['body'])
            if result['statusCode'] == 200:
                st.session_state.step3_done = True
                st.session_state.step3_output = (
                    f"Status: {result['statusCode']} OK\n"
                    f"Message: {body['message']}\n"
                    f"Insights Generated: {body['insights_count']}\n"
                    f"S3 Key: analyze/processed/{datetime.now().strftime('%Y-%m-%d')}/vendor_insights.json"
                )
            else:
                st.session_state.step3_output = f"ERROR: {body.get('error', 'Unknown')}"
        st.rerun()
    if disabled:
        st.caption("⚠️ Complete Step 2 first")

with right:
    if st.session_state.step3_output:
        st.markdown("**Lambda Output**")
        st.code(st.session_state.step3_output, language="bash")

    if st.session_state.step3_done:
        date_str = datetime.now().strftime('%Y-%m-%d')
        data = load_json(
            f"data/lake/vendor_insights_{date_str}.json",
            f"analyze/processed/{date_str}/vendor_insights.json"
        )
        if data and data['insights']:
            st.markdown("**Sample Bedrock Insight:**")
            for insight in data['insights'][:2]:
                with st.expander(f"🏙️ {insight['city']}"):
                    st.write(f"📍 **Location:** {insight.get('location', 'N/A')}")
                    st.write(f"🛒 **Recommended Product:** {insight.get('recommended_product', 'N/A')}")
                    st.write(f"💰 **Price Advice:** {insight.get('fair_price_advice', 'N/A')}")
                    st.write(f"⏰ **Golden Hour:** {insight.get('golden_hour', 'N/A')}")
                    st.write(f"📝 **Summary:** *{insight.get('summary', 'N/A')}*")

st.markdown("---")

# ══════════════════════════════════════════════════════════
# STEP 4 — DELIVER
# ══════════════════════════════════════════════════════════
st.markdown("## Step 4 — 📱 SMS Delivery")

left, right = st.columns([1, 2])

with left:
    st.markdown("Amazon Translate localizes the insight into the vendor's language. Twilio delivers it as SMS to a basic mobile phone — no internet required.")
    st.markdown("")
    st.markdown("**AWS Services**")
    st.markdown("""
- 🟠 **Amazon Translate** — localizes to Hindi / Tamil / Telugu / Kannada
- 🟠 **Amazon S3** — reads vendor insights from Data Lake
- 🔴 **Twilio** — SMS delivery to basic phone
    """)
    st.markdown(f"**Status:** {badge(st.session_state.step4_done)}")
    disabled = not st.session_state.step3_done
    if st.button("▶  Run Deliver Lambda", use_container_width=True, type="primary", key="btn4", disabled=disabled):
        # Build SMS preview text before calling
        date_str = datetime.now().strftime('%Y-%m-%d')
        idata = load_json(
            f"data/lake/vendor_insights_{date_str}.json",
            f"analyze/processed/{date_str}/vendor_insights.json"
        )
        if idata and idata['insights']:
            target = next((x for x in idata['insights'] if x['city'] == 'Chennai'), None)
            if not target:
                target = idata['insights'][0]
            if target:
                st.session_state.sms_text = (
                    f"SignalWorks: {target['summary']} "
                    f"{target['fair_price_advice']}. "
                    f"Golden Hour: {target['golden_hour']}."
                )
        with st.spinner("Lambda running — translating and sending via Twilio..."):
            from functions.deliver.handler import lambda_handler as deliver_handler
            result = deliver_handler({}, None)
            body = json.loads(result['body'])
            if result['statusCode'] == 200:
                st.session_state.step4_done = True
                results_text = "\n".join(
                    f"  · Vendor {r['vendor_id']} ({r['city']}): {r['status']}"
                    for r in body.get('results', [])
                )
                st.session_state.step4_output = (
                    f"Status: {result['statusCode']} OK\n"
                    f"Message: {body['message']}\n"
                    f"Total Sent: {body['total_sent']}\n"
                    f"{results_text}"
                )
            else:
                st.session_state.step4_output = f"ERROR: {body.get('error', 'Unknown')}"
        st.rerun()
    if disabled:
        st.caption("⚠️ Complete Step 3 first")

with right:
    if st.session_state.step4_output:
        st.markdown("**Lambda Output**")
        st.code(st.session_state.step4_output, language="bash")

    if st.session_state.step4_done and st.session_state.sms_text:
        st.markdown("**📨 SMS Delivered to +918681980569**")
        st.markdown(
            f"""
            <div style="
                background: #0d1117;
                border-radius: 16px;
                padding: 20px 24px;
                font-size: 15px;
                color: #e6edf3;
                border-left: 4px solid #FF9900;
                max-width: 500px;
                margin-top: 8px;
                line-height: 1.6;
            ">
                <div style="color:#FF9900; font-size:11px; margin-bottom:10px; letter-spacing:1px;">
                    📡 SIGNALWORKS &nbsp;·&nbsp; {datetime.now().strftime('%I:%M %p')} &nbsp;·&nbsp; Twilio via Amazon Translate
                </div>
                {st.session_state.sms_text}
            </div>
            """,
            unsafe_allow_html=True
        )

# ── Footer ─────────────────────────────────────────────────
st.markdown("---")
st.caption("SignalWorks · Built on AWS · Bharat AI Hackathon · Lambda · S3 · Bedrock · SageMaker · Translate · EventBridge")
