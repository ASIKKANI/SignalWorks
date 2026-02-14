# Requirements Document: SignalWorks

## Introduction

SignalWorks (Mandi in Your Pocket) is an AI-powered Market Intelligence platform designed for India's 10+ million street vendors who operate with basic feature phones and limited connectivity. The platform addresses the "Triple Uncertainty" problem vendors face daily: Spatial Uncertainty (where to sell), Temporal Uncertainty (when to sell), and Pricing Uncertainty (fair market rates). SignalWorks delivers actionable, location-specific intelligence via SMS and IVR to basic 2G-enabled feature phones, leveraging AWS AI services to democratize market access and increase vendor earnings.

## Glossary

- **Vendor**: Street vendor or hawker using the SignalWorks platform
- **Platform**: The SignalWorks system including all modules and services
- **Revenue_Heatmap**: Aggregated visualization of predicted high-footfall locations
- **Golden_Hour_SMS**: Daily morning SMS alert with location and pricing recommendations
- **Cell_Tower_Triangulation**: Method to infer vendor location using mobile network data
- **IVR_System**: Interactive Voice Response system for voice-based queries
- **Fair_Pricing_Engine**: Component that calculates optimal retail prices
- **Scheme_Bot**: RAG-based assistant for government scheme information
- **Sidewalk_Intelligence_Engine**: Core reasoning engine that analyzes multiple data sources
- **Registration_System**: Zero-touch activation module for vendor onboarding
- **Alert_Delivery_System**: SMS and voice notification infrastructure
- **Knowledge_Base**: Vector store containing government scheme documents
- **Vendor_Profile**: Stored information about vendor including trade, location, language preference
- **Reason_Code**: Human-readable explanation for why a recommendation was generated (e.g., "Cricket Match ends at 5 PM")
- **Store-and-Forward_Buffer**: Queue system for SMS messages that cannot be delivered due to zero-signal conditions

## Requirements

### Requirement 1: Zero-Touch Vendor Registration

**User Story:** As a street vendor with a basic feature phone, I want to register for the platform using voice input in my native language, so that I can access market intelligence without needing smartphone skills or data connectivity.

#### Acceptance Criteria

1. WHEN a vendor calls the toll-free registration number, THE Registration_System SHALL answer the call and prompt for voice input in the vendor's preferred language
2. WHEN a vendor provides voice input for name, trade type, and city zone, THE Registration_System SHALL capture and store this information in the Vendor_Profile
3. WHEN registration voice input is complete, THE Registration_System SHALL send a confirmation SMS to the vendor's phone number
4. WHERE a vendor provides a Pin Code via SMS, THE Registration_System SHALL use it to determine the vendor's location zone
5. WHERE Cell Tower Triangulation data is available, THE Registration_System SHALL infer the vendor's approximate location and store it in the Vendor_Profile
6. THE Registration_System SHALL support voice input in at least three Indian languages (Hindi, Tamil, Telugu)
7. WHEN voice input contains background noise, THE Registration_System SHALL apply noise tolerance algorithms to extract vendor information accurately

### Requirement 2: Location Inference and Management

**User Story:** As a vendor without GPS capability, I want the platform to automatically determine my location, so that I receive relevant local market intelligence.

#### Acceptance Criteria

1. WHEN a vendor registers or makes a call, THE Platform SHALL attempt to infer location using Cell_Tower_Triangulation
2. IF Cell_Tower_Triangulation is unavailable, THEN THE Platform SHALL request the vendor to send their Pin Code via SMS
3. WHEN a vendor's location is successfully determined, THE Platform SHALL store the location data in the Vendor_Profile with a timestamp
4. WHEN a vendor moves to a different zone, THE Platform SHALL update the Vendor_Profile location based on new Cell_Tower_Triangulation data
5. THE Platform SHALL maintain location accuracy within a 2-kilometer radius for urban areas

### Requirement 3: Multi-Source Data Ingestion

**User Story:** As the platform, I want to continuously ingest real-time data from multiple sources, so that I can generate accurate market intelligence for vendors.

#### Acceptance Criteria

1. THE Platform SHALL ingest hyper-local event data from city calendars, temple schedules, and exam timetables on a daily basis
2. THE Platform SHALL ingest real-time traffic and transit data from Metro stations and Bus stands to estimate pedestrian footfall
3. THE Platform SHALL ingest weather forecast data including rain alerts and temperature predictions
4. THE Platform SHALL ingest daily wholesale commodity prices from e-NAM or Mandi APIs
5. WHEN any data source is unavailable, THE Platform SHALL log the failure and continue operating with available data sources
6. THE Platform SHALL store ingested data with timestamps in the historical database for trend analysis
7. WHEN data ingestion occurs, THE Platform SHALL complete the process within 15 minutes of the scheduled time

### Requirement 4: Sidewalk Intelligence Engine with Explainability

**User Story:** As the platform, I want to analyze multiple data sources using AI reasoning and provide transparent explanations, so that vendors understand and trust the recommendations they receive.

#### Acceptance Criteria

1. WHEN analyzing data sources, THE Sidewalk_Intelligence_Engine SHALL use Amazon Bedrock (Claude 3) for cross-dataset reasoning
2. WHEN generating a Revenue_Heatmap, THE Sidewalk_Intelligence_Engine SHALL correlate event data, traffic patterns, and weather conditions
3. WHEN heavy rain is predicted AND a major event is ending nearby, THE Sidewalk_Intelligence_Engine SHALL recommend covered locations near transit hubs
4. WHEN identifying high-footfall locations, THE Sidewalk_Intelligence_Engine SHALL consider the vendor's trade type and current location from the Vendor_Profile
5. WHEN predicting optimal selling time windows, THE Sidewalk_Intelligence_Engine SHALL base predictions on historical footfall patterns and current event schedules
6. WHEN generating any recommendation, THE Sidewalk_Intelligence_Engine SHALL include a human-readable Reason_Code explaining the primary factor driving the recommendation
7. THE Reason_Code SHALL specify the triggering event or condition (e.g., "Cricket Match ends at 5 PM" or "Temple Festival today" or "Rain expected at 3 PM")
8. WHEN composing recommendations for SMS or voice delivery, THE Platform SHALL include the Reason_Code in the message to build vendor trust
9. THE Sidewalk_Intelligence_Engine SHALL update the Revenue_Heatmap every 6 hours to reflect changing conditions

### Requirement 5: Dynamic Trade-Aware Golden Hour SMS Alerts

**User Story:** As a vendor, I want to receive one actionable SMS at the optimal time for my specific trade in my language, so that I can plan my day and maximize my earnings without information overload.

#### Acceptance Criteria

1. WHEN determining alert timing, THE Alert_Delivery_System SHALL dynamically calculate the optimal delivery time based on the vendor's trade type from the Vendor_Profile
2. WHERE the vendor is a Flower Seller or Morning Market vendor, THE Alert_Delivery_System SHALL send the Golden_Hour_SMS between 4:00 AM and 5:00 AM
3. WHERE the vendor is a Breakfast or Tea vendor, THE Alert_Delivery_System SHALL send the Golden_Hour_SMS between 5:30 AM and 6:30 AM
4. WHERE the vendor is a Lunch vendor, THE Alert_Delivery_System SHALL send the Golden_Hour_SMS between 9:00 AM and 10:00 AM
5. WHERE the vendor is an Evening Snack, Chaat, or Street Food vendor, THE Alert_Delivery_System SHALL send the Golden_Hour_SMS between 3:00 PM and 4:00 PM
6. WHERE the vendor is a Dinner or Night Market vendor, THE Alert_Delivery_System SHALL send the Golden_Hour_SMS between 5:00 PM and 6:00 PM
7. WHEN generating the Golden_Hour_SMS, THE Platform SHALL include the vendor's name, relevant local event, recommended location, optimal time window, suggested commodity price, and the Reason_Code explaining the recommendation
8. THE Alert_Delivery_System SHALL compose the Golden_Hour_SMS in the vendor's preferred regional language as specified in the Vendor_Profile
9. THE Golden_Hour_SMS SHALL not exceed 160 characters to ensure delivery as a single SMS message
10. WHEN the Alert_Delivery_System sends an SMS, THE Platform SHALL log the delivery status and retry up to 3 times if delivery fails
11. THE Alert_Delivery_System SHALL complete delivery of all Golden_Hour_SMS messages to 100,000 vendors within 5 minutes of their scheduled time window
12. WHEN a vendor has not updated their location in 7 days, THE Platform SHALL include a prompt to update location in the Golden_Hour_SMS

### Requirement 6: Interactive Voice Query System

**User Story:** As a vendor, I want to call and ask questions in my native dialect using natural language, so that I can get immediate answers to urgent market situations.

#### Acceptance Criteria

1. WHEN a vendor calls the IVR number, THE IVR_System SHALL answer within 3 rings and greet the vendor in their preferred language
2. THE IVR_System SHALL accept unstructured voice queries in at least three Indian dialects (Hindi, Tamil, Telugu)
3. WHEN a vendor asks a question, THE IVR_System SHALL use Amazon Lex to interpret the intent and extract relevant parameters
4. THE IVR_System SHALL query the Sidewalk_Intelligence_Engine for real-time recommendations based on the vendor's question
5. WHEN generating a voice response, THE IVR_System SHALL use Amazon Polly to synthesize natural-sounding speech in the vendor's language
6. THE IVR_System SHALL provide responses within 5 seconds of receiving the vendor's complete question
7. IF the IVR_System cannot understand the query after 2 attempts, THEN THE IVR_System SHALL offer to connect the vendor to a fallback SMS-based help system

### Requirement 7: Dynamic Fair-Pricing Engine

**User Story:** As a vendor, I want to receive fair retail price recommendations based on current wholesale rates, so that I can avoid being exploited by middlemen and price my goods competitively.

#### Acceptance Criteria

1. THE Fair_Pricing_Engine SHALL ingest daily wholesale commodity prices from e-NAM or Mandi APIs
2. WHEN calculating retail prices, THE Fair_Pricing_Engine SHALL use Amazon SageMaker time-series forecasting to predict optimal pricing
3. THE Fair_Pricing_Engine SHALL apply a reasonable markup percentage (15-30%) over wholesale prices based on commodity type and local market conditions
4. THE Fair_Pricing_Engine SHALL include price recommendations in the Golden_Hour_SMS for the vendor's primary trade commodities
5. WHEN a vendor queries prices via IVR, THE Fair_Pricing_Engine SHALL provide current recommended retail prices within 3 seconds
6. THE Fair_Pricing_Engine SHALL implement guardrails to prevent predatory pricing recommendations (prices must be within 10% of regional average)
7. WHEN wholesale price data is unavailable for a commodity, THE Fair_Pricing_Engine SHALL use the most recent available price with a staleness indicator

### Requirement 8: Government Scheme Assistant (RAG)

**User Story:** As a vendor, I want to easily discover and understand government financial schemes available to me, so that I can access loans and benefits without navigating complex bureaucracy.

#### Acceptance Criteria

1. WHEN a vendor sends an SMS with keywords like "Loan help" or "Scheme", THE Scheme_Bot SHALL trigger a search in the Knowledge_Base
2. THE Scheme_Bot SHALL use Amazon Bedrock Knowledge Bases with RAG to search government scheme documents including PM SVANidhi
3. WHEN relevant schemes are found, THE Scheme_Bot SHALL generate a simplified 3-step application guide
4. THE Scheme_Bot SHALL send the scheme information via SMS in the vendor's preferred language within 30 seconds
5. THE Scheme_Bot SHALL include a helpline number or website link for further assistance in the response SMS
6. THE Knowledge_Base SHALL be updated monthly with the latest government scheme documents and eligibility criteria
7. WHEN multiple schemes match the vendor's query, THE Scheme_Bot SHALL prioritize schemes based on vendor eligibility from the Vendor_Profile

### Requirement 9: Resilient Alert Delivery with Store-and-Forward

**User Story:** As the platform operator, I want to reliably deliver SMS alerts to hundreds of thousands of vendors even in zero-signal zones, so that all vendors receive timely market intelligence regardless of network conditions.

#### Acceptance Criteria

1. THE Alert_Delivery_System SHALL handle delivery of 100,000 SMS messages within 5 minutes of scheduled time during peak hours
2. WHEN SMS delivery fails due to network issues, THE Alert_Delivery_System SHALL implement exponential backoff retry logic with up to 3 immediate retry attempts
3. IF a vendor's phone is in a zero-signal zone (no network connectivity), THEN THE Alert_Delivery_System SHALL queue the SMS message in a Store-and-Forward buffer
4. WHEN a message is in the Store-and-Forward buffer, THE Alert_Delivery_System SHALL attempt redelivery every 2 hours for up to 24 hours
5. WHEN a vendor's phone reconnects to the network, THE Alert_Delivery_System SHALL immediately attempt delivery of all queued messages
6. THE Alert_Delivery_System SHALL prioritize delivery of the most recent Golden_Hour_SMS if multiple messages are queued for a vendor
7. THE Alert_Delivery_System SHALL use Amazon Pinpoint or Amazon SNS for SMS gateway services
8. THE Alert_Delivery_System SHALL maintain a delivery success rate of at least 95% within 24 hours across all vendors
9. WHEN 2G network connectivity is intermittent, THE Alert_Delivery_System SHALL detect successful delivery confirmation before marking a message as delivered
10. THE Alert_Delivery_System SHALL log all delivery attempts, successes, failures, and retry events with timestamps for monitoring
11. THE Platform SHALL scale automatically to handle up to 500,000 concurrent vendors without degradation in delivery time

### Requirement 10: Voice Call Infrastructure

**User Story:** As the platform operator, I want to provide reliable voice interaction capabilities, so that vendors can access the platform even when SMS is not convenient.

#### Acceptance Criteria

1. THE IVR_System SHALL use Amazon Connect for call handling and routing
2. THE IVR_System SHALL support at least 1,000 concurrent voice calls without call drops
3. WHEN call volume exceeds capacity, THE IVR_System SHALL queue callers with an estimated wait time announcement
4. THE IVR_System SHALL maintain call audio quality suitable for understanding speech in noisy street environments
5. THE IVR_System SHALL log all call sessions including duration, intent recognized, and response provided
6. WHEN a call is disconnected unexpectedly, THE IVR_System SHALL send a follow-up SMS with the answer to the vendor's query
7. THE IVR_System SHALL operate on toll-free numbers to ensure zero cost for vendors

### Requirement 11: Data Storage and Vendor Profile Management

**User Story:** As the platform, I want to efficiently store and retrieve vendor profiles and historical data, so that I can provide personalized recommendations and analyze trends.

#### Acceptance Criteria

1. THE Platform SHALL store Vendor_Profile data in Amazon DynamoDB with vendor phone number as the primary key
2. THE Platform SHALL store historical event data, pricing data, and recommendation outcomes in Amazon Aurora Serverless
3. WHEN a Vendor_Profile is created or updated, THE Platform SHALL complete the operation within 100 milliseconds
4. THE Platform SHALL maintain data consistency across all storage systems
5. THE Platform SHALL implement data retention policies to archive data older than 2 years
6. THE Platform SHALL encrypt all vendor data at rest and in transit
7. WHEN querying vendor data for recommendation generation, THE Platform SHALL retrieve results within 50 milliseconds

### Requirement 12: Batch Processing and Orchestration

**User Story:** As the platform, I want to orchestrate daily batch processing of data ingestion, analysis, and alert generation, so that vendors receive timely and accurate recommendations.

#### Acceptance Criteria

1. THE Platform SHALL trigger data ingestion Lambda functions on a CRON schedule at 5:00 AM daily
2. WHEN data ingestion completes, THE Platform SHALL automatically trigger the Sidewalk_Intelligence_Engine analysis at 6:00 AM
3. WHEN analysis completes, THE Platform SHALL automatically trigger Golden_Hour_SMS generation and delivery
4. THE Platform SHALL use AWS Lambda for all batch processing and orchestration tasks
5. IF any batch processing step fails, THEN THE Platform SHALL send alerts to platform operators and attempt recovery
6. THE Platform SHALL complete the entire batch pipeline from ingestion to SMS delivery within 60 minutes
7. THE Platform SHALL log all batch processing steps with timestamps and success/failure status

### Requirement 13: Feedback Loop and Heatmap Updates

**User Story:** As the platform, I want to collect vendor location data and outcomes to continuously improve recommendations, so that the intelligence engine becomes more accurate over time.

#### Acceptance Criteria

1. WHEN a vendor makes an IVR call or sends an SMS, THE Platform SHALL update the vendor's current location in the Vendor_Profile
2. THE Platform SHALL aggregate anonymized vendor location data to update the Live Revenue_Heatmap
3. THE Platform SHALL use vendor location patterns to identify emerging high-footfall areas
4. WHEN the Revenue_Heatmap is updated, THE Platform SHALL make the new data available to the Sidewalk_Intelligence_Engine within 10 minutes
5. THE Platform SHALL maintain vendor privacy by aggregating data at the zone level (minimum 50 vendors per zone)
6. THE Platform SHALL track recommendation outcomes by correlating vendor locations with recommended locations
7. THE Platform SHALL use outcome data to retrain the Fair_Pricing_Engine models monthly

### Requirement 14: Responsible AI and Guardrails

**User Story:** As the platform operator, I want to ensure AI-generated recommendations are fair, safe, and beneficial to vendors, so that the platform builds trust and avoids harm.

#### Acceptance Criteria

1. THE Fair_Pricing_Engine SHALL implement guardrails to prevent predatory pricing recommendations
2. THE Platform SHALL ensure all price recommendations are within 10% of regional average retail prices
3. THE Platform SHALL not recommend locations that are legally restricted for street vending
4. THE Sidewalk_Intelligence_Engine SHALL avoid generating recommendations that could lead to vendor overcrowding at a single location
5. THE Platform SHALL use aggregated and anonymized data for all analytics to protect vendor privacy
6. THE Platform SHALL provide vendors with the ability to opt-out of data collection via SMS command
7. WHEN AI-generated content is sent to vendors, THE Platform SHALL include a disclaimer that recommendations are advisory only

### Requirement 15: Multi-Language Support

**User Story:** As a vendor who speaks a regional Indian language, I want all platform interactions in my native language, so that I can fully understand and benefit from the service.

#### Acceptance Criteria

1. THE Platform SHALL support at least three Indian languages: Hindi, Tamil, and Telugu
2. WHEN a vendor registers, THE Registration_System SHALL detect or ask for the vendor's preferred language
3. THE Platform SHALL store language preference in the Vendor_Profile
4. THE Alert_Delivery_System SHALL compose all SMS messages in the vendor's preferred language
5. THE IVR_System SHALL conduct all voice interactions in the vendor's preferred language
6. THE Scheme_Bot SHALL provide government scheme information in the vendor's preferred language
7. THE Platform SHALL use culturally appropriate greetings and terminology for each supported language

### Requirement 16: Platform Monitoring and Reliability

**User Story:** As the platform operator, I want comprehensive monitoring and alerting, so that I can ensure high availability and quickly resolve issues affecting vendors.

#### Acceptance Criteria

1. THE Platform SHALL monitor SMS delivery success rates and alert operators when rates fall below 90%
2. THE Platform SHALL monitor IVR call success rates and alert operators when rates fall below 95%
3. THE Platform SHALL monitor API response times and alert operators when latency exceeds 5 seconds
4. THE Platform SHALL monitor data ingestion job success and alert operators when jobs fail
5. THE Platform SHALL maintain system uptime of at least 99.5% excluding planned maintenance
6. THE Platform SHALL log all errors with sufficient context for debugging and resolution
7. THE Platform SHALL provide a dashboard showing real-time metrics for all critical system components

### Requirement 17: Cost Optimization

**User Story:** As the platform operator, I want to minimize operational costs while maintaining service quality, so that the platform remains financially sustainable.

#### Acceptance Criteria

1. THE Platform SHALL use AWS Lambda for compute to pay only for actual execution time
2. THE Platform SHALL use Amazon Aurora Serverless to automatically scale database capacity based on demand
3. THE Platform SHALL cache frequently accessed data to reduce database query costs
4. THE Platform SHALL use Amazon Bedrock on-demand pricing to avoid paying for idle AI capacity
5. THE Platform SHALL implement SMS message optimization to minimize character count without losing clarity
6. THE Platform SHALL monitor AWS costs daily and alert operators when spending exceeds budget thresholds
7. THE Platform SHALL archive historical data to lower-cost storage tiers after 90 days

### Requirement 18: Security and Access Control

**User Story:** As the platform operator, I want robust security controls, so that vendor data is protected and the platform is resilient against attacks.

#### Acceptance Criteria

1. THE Platform SHALL encrypt all data at rest using AWS KMS
2. THE Platform SHALL encrypt all data in transit using TLS 1.2 or higher
3. THE Platform SHALL implement IAM roles with least-privilege access for all AWS services
4. THE Platform SHALL authenticate all API calls using AWS Signature Version 4
5. THE Platform SHALL implement rate limiting on IVR and SMS endpoints to prevent abuse
6. THE Platform SHALL log all access to vendor data for audit purposes
7. THE Platform SHALL conduct security vulnerability scans monthly and remediate critical issues within 7 days
