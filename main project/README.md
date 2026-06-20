# LogSense: Multi-Domain Intelligent Diagnostic Assistant
**Team Aarohan | Offline AI Diagnostic Tool for Medical, Mechanical, and IT Logs**

## The Problem & Our Solution
**The Problem:** In remote clinics, factory floors, or offline server rooms, non-expert staff cannot decipher complex machine, medical, or IT logs without an expert present or an active internet connection.
**The Solution:** LogSense processes raw log text instantly and completely offline. Using a hybrid Machine Learning and Rule-Based engine, it outputs the exact severity, diagnosis, cause, and actionable fix steps.

## Key Features
* **100% Offline AI:** Runs completely locally without internet using a lightweight Scikit-Learn model.
* **Multi-Domain Support:** Dynamically categorizes logs across Medical, Machine, and IT domains.
* **Local History Tracking:** Uses SQLite to store all past diagnoses securely on the device.
* **Automated Reporting:** Generates instant, downloadable PDF diagnostic reports.

## System Architecture
`User Input Log` ➔ `Flask Backend` ➔ `ML Engine (Predicts Domain)` ➔ `JSON Rule Matcher` ➔ `Result Display` ➔ `PDF Report / SQLite Save`

## Folder Structure
```text
LogSense/
│
├── backend/
│   ├── app.py
│   ├── database.py
│   ├── pdf_generator.py
│   └── requirements.txt
│
└── model/
    ├── predict.py
    ├── classifier.pkl
    └── rules/
        ├── medical.json
        ├── machine.json
        └── it.json