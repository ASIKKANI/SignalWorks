# SignalWorks - "Morning Intelligence" for Bharat

SignalWorks is a serverless, AI-powered "Zero-UI" solution designed to empower Indian street vendors, farmers, and daily wage earners with hyper-localized, actionable intelligence. Delivered via SMS before 6:00 AM, it provides critical insights on weather, market demand, fair pricing, and government schemes, enabling them to make informed daily business decisions without requiring a smartphone or internet proficiency.

## ☁️ Where AWS is Used
The entire architecture is 100% serverless and built natively on AWS to ensure maximum scalability, high availability, and optimal cost-efficiency:

*   **AWS Lambda**: Serverless compute running the core business logic across multiple discrete microservices (`ingest`, `predict`, `analyze`, `deliver`, `feedback`, `scheme_bot`).
*   **Amazon DynamoDB**: Fast, NoSQL database used to store user profiles, locations, roles, and language preferences.
*   **Amazon S3**: Acts as a Data Lake (`signalworks-data-lake`) to store ingested daily raw data (weather, Mandi prices, traffic).
*   **Amazon EventBridge**: Used for scheduling the daily morning broadcast pipeline.
*   **Amazon API Gateway**: To expose secure HTTP endpoints for onboarding, twilio webhooks, and the Scheme Bot interaction.

## 🤖 AI on AWS: Tools & Usage

### What AI Tools are Used?
The project heavily relies on **Amazon Bedrock**, specifically using the **Anthropic Claude 3 Haiku** foundation model (`anthropic.claude-3-haiku-20240307-v1:0`), due to its speed, affordability, and excellent multilingual capabilities.

### Why is AI Used in this Project?
Handling the diverse unstructured realities of the Indian informal economy requires an intelligence layer that standard code cannot provide. AI is used to:
1.  **Synthesize Complex Data**: Transforming raw JSON from weather APIs and Mandi agricultural price boards into a cohesive, conversational summary.
2.  **Hyper-Personalization**: Generating insights specific to a user's role (e.g., advising a mango vendor differently than a cotton farmer) and their exact location.
3.  **Language Localization**: Instantly translating complex agricultural/business advice into the user's preferred regional language (Hindi, Tamil, Telugu, Kannada) directly using LLM translation capabilities.
4.  **Sentiment & Intent Analysis**: Processing incoming unstructured feedback via SMS to determine if a user found the insight helpful, or identifying when a user is specifically asking a question about government incentives.

## 🔄 System Workflow & Architecture

The system operates through an automated pipeline divided into several decoupled Lambda functions:

### 1. Ingestion (`ingest`)
*   **Action**: New users are onboarded into the platform. Their data (Phone Number, Role, City, Language Preference) is saved into **Amazon DynamoDB**.

### 2. Prediction / Data Gathering (`predict`)
*   **Action**: Triggered early in the morning via **EventBridge**, this phase fetches raw macro-environmental data.
*   **Details**: It pulls 5-day weather forecasts from OpenWeather and agricultural prices from Agmarknet, transforming this data and dumping it into the **Amazon S3 Data Lake** for the day.

### 3. AI Analysis (`analyze`)
*   **Action**: Consolidates user profiles and the daily environmental data to generate insights.
*   **Details**: Reads the user profiles from DynamoDB and the daily weather/market conditions from S3. It passes this context into **Amazon Bedrock (Claude 3)** with a prompt instructing it to act as an expert agricultural business advisor. The AI outputs a tailored Action Plan for the day (e.g., "Heavy rain expected by 2 PM, sell perishables early or arrange tarpaulins").

### 4. Zero-UI Delivery (`deliver`)
*   **Action**: Sends the insight to the user's basic mobile phone.
*   **Details**: Takes the English AI insight generated in the Analyze step and uses **Amazon Bedrock** again to accurately translate it into the user's native tongue. It then interfaces with **Twilio** (or Amazon Pinpoint/SNS) to dispatch the insight as a standard SMS text message.

### 5. Continuous Feedback (`feedback`)
*   **Action**: Users can reply to the SMS to share ground truth or rate the prediction.
*   **Details**: The webhook triggers a Lambda function that uses **Amazon Bedrock** to run sentiment analysis on the reply. If the AI detects an issue (e.g., "The price was actually much lower"), this ground-truth data is logged to refine future AI system prompts.

### 6. Interactive Scheme Bot (`scheme_bot`)
*   **Action**: A conversational SMS bot helping farmers discover government benefits.
*   **Details**: If a user texts a query like "Am I eligible for PM-Kisan?", this Lambda triggers, retrieves their profile from DynamoDB, and uses **Amazon Bedrock** to cross-reference their profile with government scheme guidelines, replying instantly via SMS in their native language.
