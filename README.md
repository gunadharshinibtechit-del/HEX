# HEX – Human-in-the-Loop Explainability

### Explainable AI for Transparent and Human-Centered Decisions

## 📌 About the Project

HEX (Human-in-the-Loop Explainability via Deep Reinforcement Learning) is an AI-based decision-support prototype that evaluates scholarship applicants and recommends whether they should be considered for a merit scholarship. It provides understandable recommendations while keeping humans involved in the final decision-making process.

## 🎯 Objectives

* Evaluate scholarship applicants using configurable criteria.
* Generate explainable recommendations.
* Allow human reviewers to agree, disagree, request more information, or override decisions.
* Promote transparency, accountability, and responsible AI.
* Support adaptation to different application domains.

## ✨ Key Features

* **Applicant Evaluation:** Enter applicant details through a user-friendly interface.
* **AI-Assisted Recommendation:** Calculate a score and suggest a decision.
* **Explainable Results:** Display factors influencing the recommendation.
* **Human-in-the-Loop Review:** Let reviewers make the final decision.
* **Configurable Architecture:** Modify evaluation fields, scoring weights, and thresholds.
* **Reusable Framework:** Adapt the system to other decision-support applications.

## 🛠️ Technology Stack

* **Backend:** Python, Flask
* **Frontend:** HTML, CSS, JavaScript
* **Database:** SQLite
* **Configuration:** Python configuration file

## ⚙️ Installation and Setup

1. Clone the repository:

   ```bash
   git clone <your-repository-url>
   ```

2. Navigate to the project folder:

   ```bash
   cd HEX_Prototype_Updated
   ```

3. Create a virtual environment:

   ```bash
   python -m venv .venv
   ```

4. Activate the environment on Windows:

   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```

5. Install dependencies:

   ```bash
   python -m pip install -r requirements.txt
   ```

6. Run the application:

   ```bash
   python app.py
   ```

7. Open your browser and visit:

   `http://127.0.0.1:5000`

## 🔧 Configuration

Modify `config.py` to customize applicant fields, evaluation weights, decision thresholds, and reviewer options. Update the evaluation logic when introducing new criteria or adapting the project to another domain.

## 🔄 Workflow

1. Enter applicant details.
2. Evaluate the submitted information.
3. View the recommendation and explanation.
4. Review the recommendation as a human decision-maker.
5. Agree, disagree, request more information, or override the result.
6. Record the human review decision.

## 🚀 Applications

* Merit scholarship evaluation
* Student admission support
* Employee performance evaluation
* Research grant assessment
* Project funding decisions

## ⚠️ Disclaimer

This is a decision-support prototype. Its recommendations are not guaranteed to be accurate or fair. Final scholarship decisions should follow official eligibility policies and human verification. The current scoring-based prototype should not be described as a trained Deep Reinforcement Learning model unless that capability is implemented.

## 👥 Project Theme

**Humanizing Technology through Explainable and Responsible AI**

HEX aims to combine automated evaluation with human judgment to support transparent, accountable, and trustworthy decisions.
