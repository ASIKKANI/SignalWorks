# Implementation Tasks: SignalWorks

## Overview

This implementation plan is structured as a **Phased Execution Roadmap** to demonstrate strategic prioritization for the AWS AI for Bharat Hackathon. The phases balance rapid MVP delivery with production-ready architecture, ensuring we can deliver a compelling demo while showcasing enterprise-grade design thinking.

**Timeline**: 2-week hackathon sprint + post-hackathon hardening

---

## Phase 1: Hackathon MVP (The "Happy Path")

**Goal**: Build the core intelligence pipeline that demonstrates AI-powered market recommendations via SMS. Focus on the "wow factor" flows that judges will evaluate.

**Duration**: Days 1-10 (Hackathon submission deadline)

### 1.1 AWS Foundation Setup

- [ ] 1.1.1 Create AWS account and configure billing alerts
- [ ] 1.1.2 Set up basic IAM roles for Lambda, DynamoDB, and Bedrock access
- [ ] 1.1.3 Configure AWS CLI and credentials for development
- [ ] 1.1.4 Create S3 bucket for raw data storage (`signalworks-raw-data`)
- [ ] 1.1.5 Create S3 bucket for scheme documents (`signalworks-scheme-docs`)

### 1.2 Core Data Layer (DynamoDB Tables)

- [ ] 1.2.1 Create `SignalWorks-Vendors` table with PhoneNumber as partition key
  - [ ] 1.2.1.1 Add TradeTypeIndex GSI (TradeType, PreferredAlertTime)
  - [ ] 1.2.1.2 Add LocationIndex GSI (Geohash prefix)
- [ ] 1.2.2 Create `SignalWorks-Events` table with EventID and StartTime
  - [ ] 1.2.2.1 Add GeohashIndex GSI for location-based queries
  - [ ] 1.2.2.2 Configure TTL attribute for auto-deletion
- [ ] 1.2.3 Create `SignalWorks-Prices` table with Commodity and Date
  - [ ] 1.2.3.1 Configure TTL for 24-hour price expiry
- [ ] 1.2.4 Seed dummy vendor data (50 test vendors across different trades)
- [ ] 1.2.5 Seed dummy event data (10 events: temple festival, cricket match, rain alert)
- [ ] 1.2.6 Seed dummy price data (5 commodities: Tomato, Onion, Flowers, Tea, Snacks)

### 1.3 Data Ingestion Lambda (Simplified for MVP)

- [ ] 1.3.1 Create `IngestCityData_Fn` Lambda function (Python 3.12)
- [ ] 1.3.2 Implement mock API fetchers (return hardcoded JSON for demo)
  - [ ] 1.3.2.1 Mock city events API (returns 3 events)
  - [ ] 1.3.2.2 Mock weather API (returns rain forecast)
  - [ ] 1.3.2.3 Mock mandi prices API (returns 5 commodity prices)
- [ ] 1.3.3 Implement data normalization and geohash conversion
- [ ] 1.3.4 Write normalized data to DynamoDB Events and Prices tables
- [ ] 1.3.5 Write raw data to S3 for audit trail
- [ ] 1.3.6 Add basic error logging to CloudWatch
- [ ] 1.3.7 Test Lambda function manually with sample event

### 1.4 Amazon Bedrock Integration

- [ ] 1.4.1 Enable Amazon Bedrock in AWS account
- [ ] 1.4.2 Request access to Claude 3 Sonnet model
- [ ] 1.4.3 Create test script to verify Bedrock API connectivity
- [ ] 1.4.4 Build prompt template for location recommendations
  - [ ] 1.4.4.1 Include vendor context (name, trade, location)
  - [ ] 1.4.4.2 Include event context (nearby events, weather)
  - [ ] 1.4.4.3 Request structured output (recommendation + reason_code)
- [ ] 1.4.5 Test prompt with 5 different vendor scenarios
- [ ] 1.4.6 Validate that Bedrock returns reason codes in responses

### 1.5 Golden Hour SMS Generation Lambda

- [ ] 1.5.1 Create `GenerateAdvice_Fn` Lambda function (Python 3.12)
- [ ] 1.5.2 Implement vendor query by TradeType using GSI
- [ ] 1.5.3 Implement nearby events query using geohash
- [ ] 1.5.4 Build Bedrock integration for recommendation generation
- [ ] 1.5.5 Implement SMS composition logic
  - [ ] 1.5.5.1 Include vendor name, event, location, time, price, reason code
  - [ ] 1.5.5.2 Enforce 160-character limit with truncation
  - [ ] 1.5.5.3 Add Hindi transliteration support (use basic library)
- [ ] 1.5.6 Add mock price prediction (hardcoded markup for MVP)
- [ ] 1.5.7 Test SMS composition for all trade types
- [ ] 1.5.8 Validate SMS character count compliance

### 1.6 Amazon Pinpoint SMS Delivery

- [ ] 1.6.1 Set up Amazon Pinpoint project
- [ ] 1.6.2 Configure SMS channel with origination number
- [ ] 1.6.3 Request production SMS access (if needed for demo)
- [ ] 1.6.4 Integrate Pinpoint SDK in `GenerateAdvice_Fn`
- [ ] 1.6.5 Implement SMS sending with delivery status logging
- [ ] 1.6.6 Test SMS delivery to 3 real phone numbers
- [ ] 1.6.7 Verify SMS arrives in correct language (Hindi)
- [ ] 1.6.8 Log delivery success/failure to CloudWatch

### 1.7 EventBridge Orchestration

- [ ] 1.7.1 Create EventBridge rule for data ingestion (5:00 AM daily)
- [ ] 1.7.2 Create EventBridge rules for trade-specific SMS delivery
  - [ ] 1.7.2.1 Flower Sellers: 4:00 AM
  - [ ] 1.7.2.2 Tea Vendors: 5:30 AM
  - [ ] 1.7.2.3 Lunch Vendors: 9:00 AM
  - [ ] 1.7.2.4 Snack Vendors: 3:00 PM
- [ ] 1.7.3 Configure EventBridge to pass trade_type parameter to Lambda
- [ ] 1.7.4 Test manual trigger of EventBridge rules
- [ ] 1.7.5 Verify end-to-end flow: EventBridge → Lambda → Bedrock → Pinpoint

### 1.8 Voice Interface (IVR) - Basic Implementation

- [ ] 1.8.1 Set up Amazon Connect instance
- [ ] 1.8.2 Claim toll-free phone number for IVR
- [ ] 1.8.3 Create basic Amazon Lex V2 bot
  - [ ] 1.8.3.1 Define GetLocationAdvice intent
  - [ ] 1.8.3.2 Define GetPriceInfo intent
  - [ ] 1.8.3.3 Add sample utterances in Hindi (transliterated)
- [ ] 1.8.4 Create `ProcessVoice_Fn` Lambda function
- [ ] 1.8.5 Implement location advice handler (calls Bedrock)
- [ ] 1.8.6 Implement price query handler (queries DynamoDB)
- [ ] 1.8.7 Configure Amazon Connect call flow
  - [ ] 1.8.7.1 Welcome message in Hindi (use Polly Aditi voice)
  - [ ] 1.8.7.2 Lex intent capture
  - [ ] 1.8.7.3 Lambda invocation
  - [ ] 1.8.7.4 Polly response synthesis
- [ ] 1.8.8 Test IVR with 3 sample queries
- [ ] 1.8.9 Record IVR interaction audio for demo video

### 1.9 Government Scheme RAG Assistant

- [ ] 1.9.1 Upload PM SVANidhi PDF documents to S3 scheme bucket
- [ ] 1.9.2 Create Amazon Bedrock Knowledge Base
- [ ] 1.9.3 Configure OpenSearch Serverless as vector store
- [ ] 1.9.4 Sync S3 bucket with Knowledge Base
- [ ] 1.9.5 Test RAG queries with sample scheme questions
- [ ] 1.9.6 Create `SchemeBot_Fn` Lambda function
- [ ] 1.9.7 Implement keyword detection for scheme queries
- [ ] 1.9.8 Integrate Bedrock Knowledge Base retrieval
- [ ] 1.9.9 Implement 3-step guide generation
- [ ] 1.9.10 Configure Pinpoint 2-way SMS webhook to trigger Lambda
- [ ] 1.9.11 Test scheme query via SMS: "Loan help"
- [ ] 1.9.12 Verify response includes simplified guide

### 1.10 Basic Monitoring & Logging

- [ ] 1.10.1 Create CloudWatch dashboard for key metrics
  - [ ] 1.10.1.1 Lambda invocation counts
  - [ ] 1.10.1.2 SMS delivery success rate
  - [ ] 1.10.1.3 Bedrock API latency
- [ ] 1.10.2 Set up CloudWatch alarm for Lambda errors (> 5%)
- [ ] 1.10.3 Set up CloudWatch alarm for SMS delivery failures (< 80%)
- [ ] 1.10.4 Enable X-Ray tracing for all Lambda functions
- [ ] 1.10.5 Test alarm triggering with intentional error

### 1.11 End-to-End Integration Testing

- [ ] 1.11.1 Test complete morning pipeline: Ingest → Analyze → SMS
- [ ] 1.11.2 Verify SMS arrives with correct content for each trade type
- [ ] 1.11.3 Test IVR call flow end-to-end
- [ ] 1.11.4 Test scheme query via SMS
- [ ] 1.11.5 Verify all CloudWatch logs are populated
- [ ] 1.11.6 Test with 10 concurrent vendor SMS deliveries
- [ ] 1.11.7 Document any bugs or issues for Phase 2

---

## Phase 2: Resilience & Production Hardening

**Goal**: Implement production-grade features that demonstrate architectural maturity: store-and-forward retry logic, security hardening, and scalability optimizations.

**Duration**: Post-hackathon (Days 11-20)

### 2.1 Store-and-Forward Retry Logic

- [ ] 2.1.1 Create `SignalWorks-FailedMessages` DynamoDB table
  - [ ] 2.1.1.1 Configure TTL for 24-hour expiry
  - [ ] 2.1.1.2 Add PhoneNumberIndex GSI for querying
- [ ] 2.1.2 Update `GenerateAdvice_Fn` to write failures to FailedMessages table
- [ ] 2.1.3 Create `RetryDelivery_Fn` Lambda function
- [ ] 2.1.4 Implement exponential backoff calculation (1h, 2h, 4h, 8h)
- [ ] 2.1.5 Implement message prioritization (most recent first)
- [ ] 2.1.6 Implement retry logic with Pinpoint
- [ ] 2.1.7 Implement DynamoDB cleanup on successful delivery
- [ ] 2.1.8 Create EventBridge rule for hourly retry trigger
- [ ] 2.1.9 Test retry flow with simulated network failure
- [ ] 2.1.10 Verify TTL auto-deletion after 24 hours

### 2.2 Amazon SageMaker Price Forecasting

- [ ] 2.2.1 Prepare historical price dataset (CSV with 90 days of data)
- [ ] 2.2.2 Create SageMaker Canvas workspace
- [ ] 2.2.3 Upload dataset and configure time-series model
- [ ] 2.2.4 Train price forecasting model (target: RecommendedRetailPrice)
- [ ] 2.2.5 Deploy model to real-time inference endpoint
- [ ] 2.2.6 Integrate SageMaker endpoint in `GenerateAdvice_Fn`
- [ ] 2.2.7 Replace mock price prediction with SageMaker calls
- [ ] 2.2.8 Implement price guardrails (15-30% markup, ±10% regional avg)
- [ ] 2.2.9 Test price predictions for 5 commodities
- [ ] 2.2.10 Validate guardrails prevent predatory pricing

### 2.3 Multi-Language Support Enhancement

- [ ] 2.3.1 Add Tamil language support to SMS composition
- [ ] 2.3.2 Add Telugu language support to SMS composition
- [ ] 2.3.3 Configure Polly voices for Tamil (Kajal) and Telugu
- [ ] 2.3.4 Update Lex bot with Tamil and Telugu utterances
- [ ] 2.3.5 Test IVR in all three languages
- [ ] 2.3.6 Test SMS delivery in all three languages
- [ ] 2.3.7 Verify culturally appropriate greetings for each language

### 2.4 Security Hardening

- [ ] 2.4.1 Create customer-managed KMS key for encryption
- [ ] 2.4.2 Enable encryption at rest for all DynamoDB tables
- [ ] 2.4.3 Enable encryption for S3 buckets (SSE-KMS)
- [ ] 2.4.4 Implement least-privilege IAM policies for all Lambda functions
- [ ] 2.4.5 Enable VPC endpoints for DynamoDB and S3 (optional)
- [ ] 2.4.6 Implement rate limiting on Pinpoint SMS endpoint
- [ ] 2.4.7 Add input validation for phone numbers (E.164 format)
- [ ] 2.4.8 Add input validation for Pin Codes (6 digits)
- [ ] 2.4.9 Implement audit logging for vendor data access
- [ ] 2.4.10 Run AWS Trusted Advisor security checks

### 2.5 Advanced Monitoring & Alerting

- [ ] 2.5.1 Expand CloudWatch dashboard with additional metrics
  - [ ] 2.5.1.1 DynamoDB read/write capacity units
  - [ ] 2.5.1.2 SageMaker endpoint invocations
  - [ ] 2.5.1.3 Bedrock token usage and costs
- [ ] 2.5.2 Create CloudWatch alarm for DynamoDB throttling
- [ ] 2.5.3 Create CloudWatch alarm for Bedrock rate limiting
- [ ] 2.5.4 Create CloudWatch alarm for daily cost exceeding budget
- [ ] 2.5.5 Set up SNS topic for operator alerts
- [ ] 2.5.6 Configure email notifications for critical alarms
- [ ] 2.5.7 Create operational runbook for common failure scenarios

### 2.6 Scalability Optimizations

- [ ] 2.6.1 Implement DynamoDB batch operations in `GenerateAdvice_Fn`
- [ ] 2.6.2 Implement Pinpoint batch API for SMS delivery (100 msgs/call)
- [ ] 2.6.3 Add Lambda reserved concurrency limits to prevent throttling
- [ ] 2.6.4 Implement caching for frequently accessed vendor profiles
- [ ] 2.6.5 Optimize Bedrock prompts to reduce token usage
- [ ] 2.6.6 Implement circuit breaker for Bedrock API failures
- [ ] 2.6.7 Test with 1,000 concurrent vendor SMS deliveries
- [ ] 2.6.8 Measure and optimize Lambda cold start times
- [ ] 2.6.9 Profile DynamoDB query performance and optimize indexes

### 2.7 Data Privacy & Compliance

- [ ] 2.7.1 Implement vendor opt-out mechanism via SMS command
- [ ] 2.7.2 Add opt-out status check before sending SMS
- [ ] 2.7.3 Implement data aggregation for heatmap (min 50 vendors/zone)
- [ ] 2.7.4 Add PII masking in CloudWatch logs
- [ ] 2.7.5 Implement data retention policy (archive after 2 years)
- [ ] 2.7.6 Create S3 lifecycle policy for Glacier transition
- [ ] 2.7.7 Add disclaimer to SMS: "Recommendations are advisory only"
- [ ] 2.7.8 Document data handling practices for compliance

### 2.8 Testing & Quality Assurance

- [ ] 2.8.1 Set up pytest testing framework
- [ ] 2.8.2 Install Hypothesis for property-based testing
- [ ] 2.8.3 Write unit tests for `IngestCityData_Fn` (5 test cases)
- [ ] 2.8.4 Write unit tests for `GenerateAdvice_Fn` (8 test cases)
- [ ] 2.8.5 Write unit tests for `ProcessVoice_Fn` (6 test cases)
- [ ] 2.8.6 Write unit tests for `RetryDelivery_Fn` (5 test cases)
- [ ] 2.8.7 Write unit tests for `SchemeBot_Fn` (5 test cases)
- [ ] 2.8.8 Implement Property 1: Registration Data Round-Trip
- [ ] 2.8.9 Implement Property 9: Reason Code Inclusion
- [ ] 2.8.10 Implement Property 13: SMS Character Limit Compliance
- [ ] 2.8.11 Implement Property 17: Price Markup Guardrails
- [ ] 2.8.12 Implement Property 24: Store-and-Forward Queueing
- [ ] 2.8.13 Run all property tests (100 examples each)
- [ ] 2.8.14 Measure code coverage (target: 85%)
- [ ] 2.8.15 Set up CI/CD pipeline with GitHub Actions

---

## Phase 3: Demo Day Prep

**Goal**: Create compelling demo materials that showcase the platform's social impact and technical excellence for hackathon judges.

**Duration**: Days 18-20 (Final 3 days before presentation)

### 3.1 Demo Video Production

- [ ] 3.1.1 Write demo script highlighting key features
  - [ ] 3.1.1.1 Problem statement: Triple Uncertainty
  - [ ] 3.1.1.2 Solution overview: SMS + IVR intelligence
  - [ ] 3.1.1.3 AWS services showcase
  - [ ] 3.1.1.4 Social impact metrics
- [ ] 3.1.2 Record vendor registration via IVR call
- [ ] 3.1.3 Capture SMS arrival on real phone (screenshot + video)
- [ ] 3.1.4 Record IVR query interaction ("Where should I sell?")
- [ ] 3.1.5 Demonstrate scheme query via SMS ("Loan help")
- [ ] 3.1.6 Show CloudWatch dashboard with live metrics
- [ ] 3.1.7 Show AWS architecture diagram animation
- [ ] 3.1.8 Record voiceover explaining technical decisions
- [ ] 3.1.9 Edit video to 3-5 minutes (hackathon requirement)
- [ ] 3.1.10 Add captions and background music

### 3.2 Live Demo Preparation

- [ ] 3.2.1 Create demo AWS account with clean data
- [ ] 3.2.2 Seed 100 realistic vendor profiles
- [ ] 3.2.3 Seed 20 realistic events (festivals, matches, exams)
- [ ] 3.2.4 Pre-warm Lambda functions to avoid cold starts
- [ ] 3.2.5 Test demo flow 5 times to ensure reliability
- [ ] 3.2.6 Prepare backup phone numbers for SMS demo
- [ ] 3.2.7 Create demo script with timing (5-minute presentation)
- [ ] 3.2.8 Prepare answers to anticipated judge questions
- [ ] 3.2.9 Test internet connectivity and AWS console access

### 3.3 Documentation & Presentation Materials

- [ ] 3.3.1 Create architecture diagram (high-resolution PNG)
- [ ] 3.3.2 Create data flow diagram for morning pipeline
- [ ] 3.3.3 Create presentation slides (15 slides max)
  - [ ] 3.3.3.1 Title slide with team info
  - [ ] 3.3.3.2 Problem statement with statistics
  - [ ] 3.3.3.3 Solution overview
  - [ ] 3.3.3.4 AWS architecture diagram
  - [ ] 3.3.3.5 Key features (SMS, IVR, RAG, Pricing)
  - [ ] 3.3.3.6 AI/ML integration (Bedrock, SageMaker)
  - [ ] 3.3.3.7 Responsible AI & guardrails
  - [ ] 3.3.3.8 Social impact metrics
  - [ ] 3.3.3.9 Scalability & cost optimization
  - [ ] 3.3.3.10 Demo screenshots
  - [ ] 3.3.3.11 Future roadmap
  - [ ] 3.3.3.12 Thank you slide
- [ ] 3.3.4 Create README.md for GitHub repository
- [ ] 3.3.5 Document API endpoints and Lambda functions
- [ ] 3.3.6 Create deployment guide (step-by-step)
- [ ] 3.3.7 Write blog post explaining technical approach

### 3.4 Screenshots & Visual Assets

- [ ] 3.4.1 Screenshot: SMS on real phone (Hindi Golden Hour alert)
- [ ] 3.4.2 Screenshot: SMS on real phone (Scheme Bot response)
- [ ] 3.4.3 Screenshot: CloudWatch dashboard with metrics
- [ ] 3.4.4 Screenshot: DynamoDB tables with sample data
- [ ] 3.4.5 Screenshot: Bedrock Knowledge Base configuration
- [ ] 3.4.6 Screenshot: Amazon Connect call flow designer
- [ ] 3.4.7 Screenshot: Pinpoint SMS delivery logs
- [ ] 3.4.8 Screenshot: Lambda function code (key sections)
- [ ] 3.4.9 Screenshot: EventBridge rules configuration
- [ ] 3.4.10 Screenshot: X-Ray service map showing request flow

### 3.5 Social Impact Narrative

- [ ] 3.5.1 Calculate potential earnings increase (15-20% for 10M vendors)
- [ ] 3.5.2 Calculate waste reduction impact (30% unsold inventory)
- [ ] 3.5.3 Estimate financial inclusion impact (5,000 scheme onboardings)
- [ ] 3.5.4 Create infographic showing impact metrics
- [ ] 3.5.5 Write vendor persona stories (Raju the flower seller)
- [ ] 3.5.6 Highlight accessibility features (2G, voice, no smartphone)
- [ ] 3.5.7 Emphasize language inclusivity (Hindi, Tamil, Telugu)
- [ ] 3.5.8 Document cost per vendor (AWS Free Tier optimization)

### 3.6 Final Testing & Rehearsal

- [ ] 3.6.1 Run full end-to-end test with fresh AWS account
- [ ] 3.6.2 Test SMS delivery to 5 different phone numbers
- [ ] 3.6.3 Test IVR with 3 different queries
- [ ] 3.6.4 Verify all CloudWatch metrics are visible
- [ ] 3.6.5 Rehearse live demo with timer (5 minutes)
- [ ] 3.6.6 Rehearse Q&A session with team
- [ ] 3.6.7 Test backup demo plan (if live demo fails)
- [ ] 3.6.8 Verify all demo materials are uploaded to submission portal

---

## Success Criteria

### Phase 1 (MVP) Success Metrics:
- [ ] End-to-end SMS delivery working for at least 3 trade types
- [ ] IVR call flow functional with 2 intents (location, price)
- [ ] Bedrock integration generating recommendations with reason codes
- [ ] Scheme Bot responding to "Loan help" SMS queries
- [ ] CloudWatch dashboard showing live metrics
- [ ] Demo video recorded and edited (3-5 minutes)

### Phase 2 (Hardening) Success Metrics:
- [ ] Store-and-forward retry logic tested with simulated failures
- [ ] SageMaker price predictions integrated with guardrails
- [ ] All 3 languages (Hindi, Tamil, Telugu) working in SMS and IVR
- [ ] Security hardening complete (encryption, IAM, rate limiting)
- [ ] Unit test coverage > 85%
- [ ] 5 property-based tests implemented and passing

### Phase 3 (Demo) Success Metrics:
- [ ] Demo video uploaded to submission portal
- [ ] Presentation slides finalized (15 slides)
- [ ] Live demo rehearsed 5+ times successfully
- [ ] All screenshots and visual assets prepared
- [ ] GitHub repository documentation complete
- [ ] Team ready for judge Q&A session

---

## Risk Mitigation

### High-Risk Items (Address in Phase 1):
1. **Bedrock Access Approval**: Request model access on Day 1 (can take 24-48 hours)
2. **Pinpoint SMS Production Access**: Request on Day 1 (can take 24 hours)
3. **Phone Number for IVR**: Claim toll-free number early (limited availability)
4. **Hindi Voice Quality**: Test Polly Aditi voice early to ensure quality

### Contingency Plans:
- **If Bedrock access delayed**: Use rule-based recommendations temporarily
- **If Pinpoint SMS fails**: Use SNS as backup SMS gateway
- **If IVR setup complex**: Focus on SMS demo, show IVR in video only
- **If SageMaker training slow**: Use mock price predictions for demo

---

## Notes for Judges

This phased approach demonstrates:
1. **Prioritization Skills**: MVP first, hardening second, polish third
2. **Production Thinking**: Phase 2 shows we understand enterprise requirements
3. **Demo Excellence**: Phase 3 ensures compelling presentation
4. **Risk Management**: Contingency plans for common AWS service delays
5. **Social Impact Focus**: Every feature ties back to vendor empowerment

The roadmap balances rapid prototyping with architectural maturity, proving we can both ship fast AND design for scale.
