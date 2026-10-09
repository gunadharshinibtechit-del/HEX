from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3, os, json
from datetime import datetime
from config import APP_TITLE, DOMAIN_LABEL, RECOMMENDATION_THRESHOLD, FIELDS, DECISION_OPTIONS

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "hex-demo-local-key")
DB_PATH = os.path.join(os.path.dirname(__file__), "hex_demo.db")

def db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with db() as conn:
        conn.execute("""CREATE TABLE IF NOT EXISTS applicants (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL, email TEXT NOT NULL, course TEXT NOT NULL,
            fields_json TEXT NOT NULL DEFAULT '{}', notes TEXT DEFAULT '',
            decision TEXT DEFAULT 'Pending', decision_reason TEXT DEFAULT '',
            created_at TEXT NOT NULL
        )""")
        # Migrate an older version of the prototype automatically.
        columns = {r["name"] for r in conn.execute("PRAGMA table_info(applicants)").fetchall()}
        if "fields_json" not in columns:
            conn.execute("ALTER TABLE applicants ADD COLUMN fields_json TEXT NOT NULL DEFAULT '{}'")
            for old_key in ("academic", "attendance", "need"):
                if old_key not in columns:
                    conn.execute(f"ALTER TABLE applicants ADD COLUMN {old_key} INTEGER NOT NULL DEFAULT 0")
            rows = conn.execute("SELECT * FROM applicants").fetchall()
            for row in rows:
                data = {}
                for f in FIELDS:
                    if f["key"] in row.keys():
                        data[f["key"]] = int(row[f["key"]])
                conn.execute("UPDATE applicants SET fields_json=? WHERE id=?", (json.dumps(data), row["id"]))
        count = conn.execute("SELECT COUNT(*) FROM applicants").fetchone()[0]
        if count == 0 and [f["key"] for f in FIELDS] == ["academic", "attendance", "need"]:
            samples = [
                ("Aarav Kumar", "aarav.demo@example.com", "B.Tech IT", {"academic":82,"attendance":91,"need":76}, "Good academic consistency."),
                ("Meera S", "meera.demo@example.com", "B.Sc Computer Science", {"academic":68,"attendance":84,"need":92}, "Requests financial support."),
                ("Rahul P", "rahul.demo@example.com", "B.Com", {"academic":91,"attendance":72,"need":48}, "Strong academics; attendance needs discussion.")
            ]
            for name,email,course,values,notes in samples:
                conn.execute("""INSERT INTO applicants(name,email,course,fields_json,notes,created_at)
                    VALUES(?,?,?,?,?,?)""",(name,email,course,json.dumps(values),notes,datetime.now().strftime("%Y-%m-%d %H:%M")))

def row_to_applicant(row):
    a = dict(row)
    try: a["field_values"] = json.loads(a.get("fields_json") or "{}")
    except (TypeError, json.JSONDecodeError): a["field_values"] = {}
    for f in FIELDS:
        a["field_values"].setdefault(f["key"], f.get("default", 0))
    weights = [max(0, float(f.get("weight", 0))) for f in FIELDS]
    total = sum(weights) or 1
    a["demo_score"] = round(sum(int(a["field_values"].get(f["key"], 0)) * w / total for f, w in zip(FIELDS, weights)))
    return a

def score_case(applicant, preference="balanced"):
    values = applicant["field_values"]
    weights = [max(0, float(f.get("weight", 0))) for f in FIELDS]
    total = sum(weights)
    if total <= 0:
        weights = [1 / max(1, len(FIELDS)) for _ in FIELDS]
    else:
        weights = [w / total for w in weights]
    if preference in ("balanced", "configured"):
        pass
    elif preference in ("academic", "attendance", "need"):
        # Compatibility with the original prototype's focus controls.
        target = {"academic":"academic", "attendance":"attendance", "need":"need"}[preference]
        if any(f["key"] == target for f in FIELDS):
            weights = [0.65 if f["key"] == target else 0.35/max(1,len(FIELDS)-1) for f in FIELDS]
    signals = []
    for f,w in zip(FIELDS, weights):
        try: value = max(0, min(100, int(values.get(f["key"], 0))))
        except (TypeError, ValueError): value = 0
        signals.append({"key":f["key"],"name":f["label"],"value":value,"weight":round(w*100,1),
                        "contribution":round(value*w,1)})
    score = round(sum(s["contribution"] for s in signals))
    recommendation = ("Recommend scholarship for human consideration" if score >= RECOMMENDATION_THRESHOLD
                      else "Do not recommend yet — review evidence and eligibility rules")
    return {"score":score,"signals":sorted(signals,key=lambda x:x["contribution"],reverse=True),
            "recommendation":recommendation,"threshold":RECOMMENDATION_THRESHOLD,
            "eligible_suggestion": score >= RECOMMENDATION_THRESHOLD}

@app.context_processor
def inject_config():
    return {"app_title": APP_TITLE, "domain_label": DOMAIN_LABEL, "config_fields": FIELDS}

@app.route("/")
def dashboard():
    with db() as conn:
        applicants = [row_to_applicant(r) for r in conn.execute("SELECT * FROM applicants ORDER BY id DESC").fetchall()]
    total=len(applicants); pending=sum(1 for a in applicants if a["decision"]=="Pending")
    return render_template("dashboard.html", applicants=applicants,total=total,pending=pending,reviewed=total-pending)

@app.route("/applicants")
def applicants_page():
    with db() as conn:
        applicants=[row_to_applicant(r) for r in conn.execute("SELECT * FROM applicants ORDER BY id DESC").fetchall()]
    return render_template("applicants.html", applicants=applicants)

@app.route("/applicants/add", methods=["GET","POST"])
def add_applicant():
    if request.method=="POST":
        name=request.form.get("name","").strip()
        email=request.form.get("email","").strip()
        course=request.form.get("course","").strip()
        values={}
        try:
            for f in FIELDS:
                value=int(request.form.get(f["key"], f.get("default",0)))
                if not 0 <= value <= 100: raise ValueError()
                values[f["key"]]=value
            if not name or not email or not course: raise ValueError()
        except ValueError:
            flash("Complete the required text fields and enter every score between 0 and 100.","error")
            return render_template("add_applicant.html", form=request.form)
        with db() as conn:
            conn.execute("""INSERT INTO applicants(name,email,course,fields_json,notes,created_at)
                VALUES(?,?,?,?,?,?)""",(name,email,course,json.dumps(values),request.form.get("notes","").strip(),datetime.now().strftime("%Y-%m-%d %H:%M")))
        flash(f"{name} was added. Open the review page to see the suggestion.","success")
        return redirect(url_for("applicants_page"))
    return render_template("add_applicant.html", form={})

@app.route("/applicants/<int:applicant_id>")
def review(applicant_id):
    with db() as conn:
        row=conn.execute("SELECT * FROM applicants WHERE id=?",(applicant_id,)).fetchone()
    if not row:
        flash("Applicant not found.","error"); return redirect(url_for("applicants_page"))
    applicant=row_to_applicant(row)
    result=score_case(applicant,request.args.get("preference","balanced"))
    return render_template("review.html",applicant=applicant,result=result,decision_options=DECISION_OPTIONS)

@app.route("/applicants/<int:applicant_id>/decision", methods=["POST"])
def save_decision(applicant_id):
    decision=request.form.get("decision","")
    reason=request.form.get("reason","").strip()
    allowed={o["value"] for o in DECISION_OPTIONS}
    if decision not in allowed:
        flash("Choose a valid human review action.","error"); return redirect(url_for("review",applicant_id=applicant_id))
    if decision in ("Human override","Disagree — do not recommend","More information needed") and not reason:
        flash("Please add a short reason for this decision.","error"); return redirect(url_for("review",applicant_id=applicant_id))
    with db() as conn:
        conn.execute("UPDATE applicants SET decision=?, decision_reason=? WHERE id=?",(decision,reason,applicant_id))
    flash("Human review action saved locally.","success")
    return redirect(url_for("review",applicant_id=applicant_id))

@app.route("/applicants/<int:applicant_id>/delete", methods=["POST"])
def delete_applicant(applicant_id):
    with db() as conn: conn.execute("DELETE FROM applicants WHERE id=?",(applicant_id,))
    flash("Applicant removed from this demo.","success")
    return redirect(url_for("applicants_page"))

@app.route("/how-it-works")
def how_it_works():
    return render_template("how_it_works.html")

init_db()
if __name__ == "__main__":
    app.run(debug=True)
