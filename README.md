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
