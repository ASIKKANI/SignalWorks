# SignalWorks — AWS Hackathon Demo Script (2 Minutes)

---

## BEFORE YOU HIT RECORD

**Terminal — clear today's S3 data for a clean run:**
```bash
cd "c:/Users/asikk/asik/Signal Work"
aws s3 rm s3://signalworks-data-lake --recursive
python -m streamlit run dashboard.py
```

**Screen layout:**
- Left half: Dashboard at **http://localhost:8501** — all 4 steps ⏳ Pending
- Right half: AWS Console → S3 → **signalworks-data-lake** bucket (empty)

Phone nearby. Volume ON. Screen visible to camera.

---

## THE VIDEO

---

### [0:00 – 0:22] HOOK

**Show:** Dashboard on left, empty S3 bucket on right

**Say:**
> "We believe vendors shouldn't have to guess their way through each day.
> That's why we built SignalWorks AI —
> a zero-UI, zero-internet SMS-based AI assistant
> that empowers vendors like Rahul to plan smarter, earn more, and sell with confidence."

*(pause 1 second)*

> "No website. No app. No login.
> Works on ANY phone — SMS arrives even without internet.
> Villages, cities, remote areas — everywhere there's mobile coverage.
> 250 million street vendors across India.
> Built entirely on AWS. Let me show you."

---

### [0:22 – 0:40] STEP 1 — DATA INGEST

**Click: ▶ Run Ingest Lambda** on the dashboard

*(while the spinner runs — speak over it)*

**Say:**
> "This is our Ingest Lambda — triggered automatically by Amazon EventBridge at 5 AM every morning.
> It's pulling live weather data from OpenWeatherMap,
> commodity prices from Agmarknet,
> and traffic congestion from Google Maps — for 6 cities across India.
> Everything gets written straight to our Amazon S3 Data Lake."

*(wait for ✅ Complete)*

**Switch to S3 console — refresh it live on camera**

> "Watch S3 — there it is.
> `ingest/raw/2026-03-08/daily_ingest.json` — just landed in the bucket."

---

### [0:40 – 0:55] STEP 2 — PRICE PREDICTION

**Click: ▶ Run Predict Lambda**

*(while spinner runs)*

**Say:**
> "Predict Lambda fires next.
> It reads the ingest data straight from S3
> and runs it through our Amazon SageMaker price model —
> calculating the fair retail price a vendor should charge today
> based on weather disruption, traffic conditions and supply trends.
> Predictions go back into S3."

*(wait for ✅ Complete — refresh S3 to show predict file appearing)*

---

### [0:55 – 1:15] STEP 3 — AI ANALYSIS

**Click: ▶ Run Analyze Lambda**

*(while spinner runs — this takes a few seconds)*

**Say:**
> "This is where AWS really shines.
> Our Analyze Lambda reads both files from S3
> and calls Amazon Bedrock — Claude 3.5 Sonnet —
> and asks it to synthesize the weather, prices, traffic and local events
> into one personalized insight for the vendor.
> Where to go. What to sell. When to be there.
> Real Generative AI — running right now in our AWS account."

*(wait for ✅ Complete)*

**Click to expand a city insight in the dashboard — show the AI-generated text**

> "This insight was written by Claude 3.5 Sonnet seconds ago —
> and it just got saved into S3."

**Refresh S3 — show vendor_insights.json appearing**

---

### [1:15 – 1:40] STEP 4 — SMS DELIVERY

**Click: ▶ Run Deliver Lambda**

*(while spinner runs)*

**Say:**
> "Final Lambda.
> It reads the Bedrock insight from S3,
> passes it through Amazon Translate to localize it —
> Hindi, Tamil, Telugu, Kannada — whichever language the vendor speaks.
> Then it fires the SMS via Twilio to a basic mobile phone.
> No app. No internet. No smartphone needed.
> Watch my phone."

*(wait for ✅ Complete — SMS preview box appears on dashboard)*

**→ HOLD PHONE UP TO CAMERA — 5 seconds of silence**

**→ SMS arrives. Let the audience read it.**

**Say:**
> "That message was generated end to end — right now — on AWS.
> Bedrock wrote it. S3 stored it. Translate localized it.
> Lambda delivered it. EventBridge will do this automatically — every single morning."

---

### [1:40 – 2:00] CLOSE

**Show:** Dashboard — all 4 steps ✅ Complete. S3 bucket with 3 files. Phone with SMS.

**Say:**
> "Amazon S3 as our data lake.
> Amazon Bedrock — Claude 3.5 Sonnet — as our AI brain.
> Amazon SageMaker for price prediction.
> Amazon Translate for 5 Indian languages.
> AWS Lambda for every step. EventBridge for the schedule.
> Zero infrastructure to manage. Zero UI for the vendor.
> Just one SMS — that changes everything."

---

## AWS SERVICES CHEAT SHEET
*(know this cold — judges will ask)*

| Service | Exactly what it does |
|---|---|
| **AWS Lambda** | Runs all 4 pipeline steps serverlessly — scales to millions of vendors |
| **Amazon EventBridge** | Triggers the pipeline at 5:00 AM, 5:30 AM, 6:00 AM daily — zero manual effort |
| **Amazon S3** | Data Lake — every step reads and writes JSON here, full audit trail |
| **Amazon Bedrock (Claude 3.5 Sonnet)** | Generates the personalized vendor insight — the AI brain of the system |
| **Amazon SageMaker** | ML endpoint for fair retail price prediction per commodity |
| **Amazon Translate** | Localizes the SMS into Hindi, Tamil, Telugu, Kannada |
| **Amazon Textract** | OCR on government scheme documents (Scheme Bot feature) |
| **Amazon DynamoDB** | Stores vendor profiles and demand heatmap feedback |

---

## IF A JUDGE ASKS "IS THIS RUNNING ON AWS RIGHT NOW?"

Say yes with full confidence:
> "Yes — completely.
> S3, Bedrock, Translate are all live in our AWS account right now.
> You can see the data files in the S3 bucket on screen.
> The Bedrock call to Claude 3.5 Sonnet happened live during this demo.
> The SMS you just saw arrive — that was triggered by a real AWS pipeline."

---

## BEFORE RECORDING CHECKLIST

- [ ] Run `aws s3 rm s3://signalworks-data-lake --recursive` to clear the bucket
- [ ] Dashboard open at http://localhost:8501 — all 4 steps ⏳ Pending
- [ ] AWS Console open — S3 bucket visible and empty
- [ ] Phone charged, volume ON, screen facing camera
- [ ] Practise the S3 refresh moment — it's your live proof of AWS
