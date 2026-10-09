
# HEX — Human-in-the-Loop Scholarship Review Prototype

A polished Flask + SQLite demo. Add an applicant, enter evidence scores, inspect a transparent weighted recommendation, and record whether the human reviewer agrees, disagrees, needs more information, or overrides it.

## Run on Windows
1. Extract the ZIP.
2. Open PowerShell inside the `HEX_Prototype_Updated` folder (the folder containing `app.py`).
3. Run:
   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   python -m pip install -r requirements.txt
   python app.py
   ```
4. Open http://127.0.0.1:5000

If PowerShell blocks activation, run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned` then activate again.

## Customize the fields for another domain
Edit **only `config.py`** for the usual changes:
- `APP_TITLE` and `DOMAIN_LABEL` update the product/domain naming.
- `FIELDS` defines the input fields shown in the form and review page.
- Each field has a unique `key`, user-facing `label`, `short_label`, `weight`, `help`, and `default`.
- `RECOMMENDATION_THRESHOLD` changes the illustrative recommendation cutoff.
- `DECISION_OPTIONS` controls the human-review choices.

Example: to switch to a project-grant review, replace `FIELDS` with keys such as `project_score`, `impact`, and `budget_fit`, with weights such as `0.4`, `0.35`, and `0.25`. Use unique keys made of lowercase letters/underscores. Keep weights non-negative; the app normalizes them automatically, though they should ideally add to 1.0. **When changing field keys after you have created records, old records won't automatically have meaningful values for the new fields**; delete `hex_demo.db` while the server is stopped to start a fresh database. Back up first if you need existing records.

## Workflow
1. Add a fictional applicant and enter scores from 0–100.
2. Open Review to see the weighted score and the reasons/signals behind it.
3. The demo suggests scholarship consideration when the score meets the configured threshold, otherwise it suggests further review.
4. The human reviewer chooses Agree, Disagree, More information needed, or Human override. The app saves that choice and the reason locally.

## Important limitations
This is **not** a trained deep reinforcement learning model and not a validated scholarship eligibility or fairness model. The score is illustrative weighted arithmetic only. Do not use it to approve or reject real scholarship applicants. Real decisions require official eligibility criteria, document verification, bias/fairness checks, and accountable human review. Use fictional data in this prototype.
=======
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

