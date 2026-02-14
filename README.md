# 🚦 SignalWorks
### Mandi in Your Pocket | AI Market Intelligence for the "Next Billion"

[![Hackathon](https://img.shields.io/badge/Competition-AWS%20AI%20for%20Bharat-FF9900?style=for-the-badge&logo=amazonaws)](https://vision.hack2skill.com/event/ai-for-bharat)
[![Status](https://img.shields.io/badge/Status-Prototype%20Ready-success?style=for-the-badge)]()
[![Stack](https://img.shields.io/badge/Tech-Bedrock%20%7C%20SageMaker%20%7C%20Pinpoint-blue?style=for-the-badge&logo=python)]()
[![License](https://img.shields.io/badge/License-MIT-lightgrey?style=for-the-badge)]()

> **"A ₹1,000 feature phone that tells a vegetable vendor exactly *where* and *when* to sell."**

<video src="https://github.com/ASIKKANI/assest/blob/main/Video_Generation_Request_Fulfilled.mp4" width="100%" controls autoplay loop muted></video>

---

## 📂 Submission Documents
**Judges, start here:**
* 📜 **[Requirements Spec](requirements.md)** → User Stories, Functional Requirements & "EARS" Syntax.
* 🏗️ **[System Architecture](design.md)** → AWS Serverless Design, Data Schema & Correctness Properties.
* ✅ **[Execution Roadmap](tasks.md)** → Phased Implementation Plan (MVP to Production).

---

## 🛑 The Problem: "Triple Uncertainty"
India's **10 Million+ street vendors** operate on gut feeling, facing three daily risks:
1.  📍 **Spatial:** "Where is the crowd today?" (Temple? Stadium? Metro?)
2.  ⏰ **Temporal:** "When should I be there?" (Morning rush vs. Evening rain?)
3.  💰 **Pricing:** "What is the fair price?" (Exploitation by middlemen.)

Most "Smart City" apps fail because **vendors don't have smartphones or data plans.**

## 💡 The Solution: SignalWorks
We don't build an app. We build a **Decision Engine** accessible via **2G**.

* **Zero-UI Interface:** Works entirely via **SMS** and **Voice Call (IVR)**.
* **Hyper-Local Intelligence:** Aggregates City Events, Traffic, and Weather to create a "Revenue Heatmap."
* **AI-Powered:** Uses **Amazon Bedrock (Claude 3)** to reason ("Go to the stadium because the match ends at 5 PM") and **SageMaker** to predict fair pricing.

---

## 🏗️ Architecture
**Event-Driven Serverless Architecture on AWS**

![Architecture Diagram](architecture_diagram.png)

* **Intelligence:** Amazon Bedrock (Reasoning) + SageMaker Canvas (Forecasting).
* **Inclusion:** Amazon Pinpoint (SMS) + Amazon Connect (Voice/IVR).
* **Scale:** AWS Lambda (Compute) + DynamoDB (Data) + EventBridge (Orchestration).

---

## 🚀 Key Features
| Feature | Tech Stack | Impact |
| :--- | :--- | :--- |
| **"Golden Hour" Alerts** | Amazon Pinpoint | Proactive SMS telling vendors exactly where to go. |
| **Voice Query (IVR)** | Amazon Connect + Polly | "Ask anything" in Hindi/Tamil/Telugu dialects. |
| **Fair Price Engine** | SageMaker Canvas | Prevents underselling by predicting daily Mandi rates. |
| **Scheme Bot (RAG)** | Bedrock Knowledge Base | Helps vendors apply for PM SVANidhi loans via SMS. |
| **Offline Mode** | DynamoDB | Store-and-forward logic for zero-signal zones. |

---

## 👥 Team: [Your Team Name]

| Name | Role | Hack2Skill ID / Reg ID |
| :--- | :--- | :--- |
| **Asik Kani** | Lead Architect | [Your ID Here] |
| **[Teammate 1 Name]** | [Role] | [ID Here] |
| **[Teammate 2 Name]** | [Role] | [ID Here] |
| **[Teammate 3 Name]** | [Role] | [ID Here] |

---

*Built with ❤️ for Bharat using AWS.*
