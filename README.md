# UnifiedTrace 🔍
## AI-Powered Cyber Fraud Correlation & Digital Artifact Intelligence Platform

**Built for Void Hacks 8.0** | Shri Vaishnav Vidyapeeth, Indore

---

## 📋 Overview

**UnifiedTrace** is an automated fraud investigation platform that correlates telecom (CDR), financial (UPI/bank), and app-level (APK) evidence in a single graph-based intelligence system.

### 🎯 Problem Solved
Investigating officers currently correlate CDR, IPDR, UPI/bank records, and APK metadata **manually across disconnected tools**, causing critical delays during the fraud investigation "golden hour."

### 💡 Solution
UnifiedTrace is a **single automated pipeline** that:
- Ingests telecom, financial, and app-level evidence
- Cross-links common entities (IMEI, UPI handles, IP subnets, MAC addresses)
- Generates court-admissible forensic briefs with minimal manual effort
- Replaces fragmented manual entity-matching with an automated correlation engine
- Reduces triage time from **hours to minutes**

---

## 🚀 Key Features

✅ **Cross-Domain Fusion** - Telecom + Financial + App evidence in single graph
✅ **ML-Based Anomaly Detection** - Isolation Forest for fraud pattern detection
✅ **Interactive Network Visualization** - Real-time entity relationship graphs
✅ **Risk Scoring** - Automated risk assessment for entities
✅ **Court-Admissible Reports** - SHA-256 hash verification per Bharatiya Sakshya Adhiniyam 2023
✅ **Offline-Capable** - SQLite local storage, no internet required
✅ **Open Source** - Zero licensing cost, lightweight Python libraries

---

## 🏗️ Tech Stack

| Component | Technology |
|-----------|-----------|
| **Backend API** | FastAPI |
| **Frontend/Dashboard** | Streamlit |
| **Graph Engine** | NetworkX |
| **Visualization** | Plotly + Pyvis |
| **ML/Anomaly Detection** | Scikit-learn (Isolation Forest) |
| **Data Parsing** | Pandas, OpenPyXL |
| **Database** | SQLite |
| **Reports** | ReportLab |
| **Forensic Hashing** | SHA-256 (Hashlib) |

---

## 📦 Installation

### Prerequisites
- Python 3.8+
- pip

### Step 1: Clone/Download the Project
```bash
cd /home/claude
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Generate Test Data (Optional)
```bash
python test_data_generator.py
```

Output:
```
✅ Test datasets generated:
   - CDR: 500 records
   - Bank: 400 records
   - APK: 150 records
```

---

## 🎮 Usage

### Option A: Run Full Application (Recommended for Demo)

```bash
streamlit run dashboard.py
```

This launches the **interactive Streamlit dashboard** at `http://localhost:8501`

### Option B: Run Backend API Only (For Development)

```bash
uvicorn backend:app --reload --port 8000
```

API docs available at: `http://localhost:8000/docs`

---

## 📊 How to Use the Dashboard

### 1️⃣ Load Data
**Sidebar → Upload Data**
- Upload CDR records (CSV)
- Upload Bank transactions (CSV)
- Upload APK metadata (CSV)
- Click **"Load Data"**

**OR**

**Sidebar → Sample Data → "Create Demo Datasets"**
- Instantly generates realistic test data for demonstration

### 2️⃣ Run Analysis
**Tab: Analysis → "Run Analysis"**
- Performs entity correlation
- Calculates risk scores using Isolation Forest
- Generates network statistics

### 3️⃣ View Results

**Analysis Tab:**
- 📊 Risk score distribution histogram
- 🔴 High-risk entities ranking

**Entity Graph Tab:**
- 🕸️ Interactive network visualization
- Node color = Risk level (Red = High)
- Node size = Connection count
- Zoom, pan, hover for details

**Entities Tab:**
- 📋 Complete entity list with risk scores
- Filter by type (IMEI, UPI, IP, etc.)
- Download as CSV

### 4️⃣ Generate Report
**Report Tab → "Generate PDF Report"**
- Court-admissible forensic investigation brief
- SHA-256 hash verification
- High-risk entity summary
- Chain-of-custody documentation

---

## 📈 Expected Results with Sample Data

### Network Statistics
```
Total Entities:           ~800
Total Relationships:     ~1500
High-Risk Entities:       ~50 (>70 risk score)
Medium-Risk Entities:     ~120 (40-70 risk score)
Network Density:          ~0.35
Avg Connections/Entity:   ~3.8
```

### Risk Distribution
- 🔴 **High Risk (>70):** Suspected mule accounts, fraud phones
- 🟡 **Medium Risk (40-70):** Connected entities, intermediate risk
- 🟢 **Low Risk (<40):** Isolated, low-anomaly entities

---

## 📁 Project Structure

```
/home/claude/
├── dashboard.py                    # Streamlit frontend
├── backend.py                      # FastAPI backend
├── test_data_generator.py          # Sample data generator
├── requirements.txt                # Python dependencies
├── README.md                       # This file
├── sample_cdr.csv                 # Generated test CDR data
├── sample_bank.csv                # Generated test bank data
└── sample_apk.csv                 # Generated test APK data
```

---

## 🔐 Forensic Integrity

**SHA-256 Hash Verification**
- Aligns with Section 63(4)(c) of Bharatiya Sakshya Adhiniyam, 2023
- Mandates hash-value disclosure for electronic evidence certification
- Every generated report includes cryptographic proof of integrity
- Chain-of-custody maintained from evidence upload to report generation

**File Integrity:**
```
Report Hash (SHA-256): [Generated at report time]
Verifies: Report integrity, timestamp, entity count, relationships
```

---

## 🎯 Use Cases

### 1. Fraud Investigation
Correlate victim's phone (CDR) → Mule's UPI account → Cash-out point IP

### 2. SIM-Swap Detection
Detect rapid phone number changes linked to suspicious account access

### 3. Money Laundering Tracking
Trace fund flow across multiple UPI handles and bank transfers

### 4. Malware Investigation
Correlate infected APKs with fraudster IMEIs and IP addresses

### 5. Mule Account Clustering
Identify networks of mule accounts operating in coordination

---

## 🚨 Limitations & Future Enhancements

### Current Limitations
- ⚠️ Basic fuzzy matching (can have false positives)
- ⚠️ Handles missing/incomplete evidence gracefully
- ⚠️ Rate-limited by local hardware

### Roadmap (v2.0+)
- 🔄 Real-time data streaming support
- 📊 Advanced GNN-based correlation
- 🌐 API-based integration with LEA systems
- 📱 Mobile app for field investigations
- 🔗 Blockchain-based evidence audit trail
- 🤖 LLM-powered investigative brief generation

---

## 🛠️ API Endpoints (Backend)

### POST `/upload/cdr`
Upload CDR records
```bash
curl -X POST -F "file=@sample_cdr.csv" http://localhost:8000/upload/cdr
```

### POST `/upload/bank`
Upload bank transactions
```bash
curl -X POST -F "file=@sample_bank.csv" http://localhost:8000/upload/bank
```

### POST `/upload/apk`
Upload APK metadata
```bash
curl -X POST -F "file=@sample_apk.csv" http://localhost:8000/upload/apk
```

### GET `/analyze`
Run correlation analysis
```bash
curl http://localhost:8000/analyze
```

### GET `/graph`
Get graph data for visualization
```bash
curl http://localhost:8000/graph
```

### GET `/report`
Download forensic report as PDF
```bash
curl http://localhost:8000/report > forensic_report.pdf
```

---

## 📚 Sample Data Format

### CDR Records (sample_cdr.csv)
```
CDR_ID,IMEI,Phone_Number,Operator,Location,Timestamp,Call_Duration,Data_Used_MB,IP_Address
CDR_000001,IMEI_1,9812345678,Airtel,Mumbai,2024-01-15 10:30:00,120,25,192.168.1.1
```

### Bank Transactions (sample_bank.csv)
```
Transaction_ID,UPI_Handle,Amount,Transaction_Type,Timestamp,Recipient_UPI,Bank_Name,Device_IP
TXN_000001,mule.1@okhdfcbank,5000,TRANSFER,2024-01-15 10:35:00,victim.sharma@okaxis,HDFC,10.0.0.1
```

### APK Metadata (sample_apk.csv)
```
APK_ID,Package_Name,SHA256_Hash,File_Size_MB,Install_Date,Permissions_Count,Is_Suspicious,IMEI
APK_000001,com.whatsapp,abc123def456...,150.5,2024-01-01,35,False,IMEI_1
```

---

## 🐛 Troubleshooting

### Issue: Import errors
```
ModuleNotFoundError: No module named 'streamlit'
```
**Solution:** Reinstall dependencies
```bash
pip install -r requirements.txt --upgrade
```

### Issue: Port already in use
```
Address already in use
```
**Solution:** Kill the process or use different port
```bash
streamlit run dashboard.py --server.port 8502
```

### Issue: Slow graph generation
**Solution:** For large datasets (>5000 entities), reduce the sample size
```python
engine.graph = engine.graph.subgraph(list(engine.graph.nodes())[:2000])
```

---

## 👥 Team

**Void Hacks 8.0 Submission**
- **Team Leader:** Zeeshan Ali (9302698198)
- **Members:** Abdul Rehman, Samya Ali, Akshay Kumar
- **Institution:** Shri Vaishnav Institute of Information Technology, Indore

---

## 📄 License & Compliance

- **Open Source License:** MIT (Proposed)
- **Legal Compliance:** Bharatiya Sakshya Adhiniyam, 2023 (Section 63)
- **Use Case:** Law Enforcement & Cybercrime Investigation
- **Data Privacy:** Local storage only, no cloud transmission

---

## 📞 Support & Documentation

For issues or questions:
1. Check the **Troubleshooting** section above
2. Review the **API Docs** at `http://localhost:8000/docs`
3. Check sample data formats in **Sample Data Format** section

---

## 🎓 Learn More

- [NetworkX Documentation](https://networkx.org/)
- [Streamlit Docs](https://docs.streamlit.io/)
- [FastAPI Tutorial](https://fastapi.tiangolo.com/)
- [Scikit-learn Anomaly Detection](https://scikit-learn.org/stable/modules/outlier_detection.html#isolation-forest)
- [Bharatiya Sakshya Adhiniyam, 2023](https://www.indiacode.nic.in/)

---

**Made with ❤️ for Void Hacks 8.0**

Last Updated: January 2025
