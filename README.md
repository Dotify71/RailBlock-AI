# 🚆 RailBlock-AI: AI-Powered Automatic Railway Block Planning Engine

**SIH 2026 Problem Statement:** `SIH26027`  
**Sponsoring Ministry:** Ministry of Railways  
**Category:** Software  
**Theme:** Transportation & Logistics  

---

## 🌟 Problem Overview
Indian Railways tracks require maintenance from 3 distinct departments:
* **P-Way (Engineering):** Track and rail repair.
* **TRD (Traction Distribution):** Overhead electrification wires.
* **S&T (Signal & Telecom):** Signals and track sensors.

Currently, these requests are submitted independently into the **Block Deduction Management System (BDMS)**, causing multiple track closures per day on the same section. **RailBlock-AI** groups multi-department requests into unified joint windows using AI constraint optimization, recovering over **40% of lost track capacity**.

---

## Quick Start Guide

### 1. Run Python Optimizer Core (CLI Test)
```bash
python3 backend/optimizer.py
```

### 2. Start REST API Server
```bash
python3 backend/app.py
```
Open `http://localhost:8000/api/optimize` in your browser or API client.

### 3. Open Interactive Web Dashboard
Open `frontend/index.html` directly in any web browser (Chrome, Edge, Safari) to launch the live demo interface for presentation!

---

## 📂 Project Structure
```
railblock-ai/
├── backend/
│   ├── app.py          # REST API server (Python http.server / FastAPI)
│   └── optimizer.py    # AI Constraint Optimization Core (OR-Tools / Clustering)
├── frontend/
│   └── index.html      # Interactive Web Dashboard (Tailwind CSS + Live Simulation)
└── README.md           # Documentation
```
