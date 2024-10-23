# Backend Engineer Trial Task by Blockhouse

This project integrates machine learning to prepare testing data, perform backtesting, fetch and store financial data in PostgreSQL, and generate PDF performance reports. The backend is built using Django and requires proper setup to run locally.

---

## Table of Contents  
- [Endpoints](#endpoints)  
- [Installation](#installation)  

---

## Endpoints

### 1. **Machine Learning Integration**  
- **URL:** `http://20.40.45.7:8000/api/predict/give_stock_code_like_AAPL,TSLA_etc/`
- **Example:** http://20.40.45.7:8000/api/predict/AAPL/
- **Method:** GET  
- **Description:**  
  Prepares testing data using machine learning models.

---

### 2. **Backtesting**  
- **URL:** `http://20.40.45.7:8000/api/backtest/?symbol=AAPL&investment=10000`  
- **Method:** GET  
- **Description:**  
  Runs backtesting on historical data for the specified symbol with a given investment amount.

---

### 3. **Fetch and Save Financial Data**  
- **URL:** `http://20.40.45.7:8000/api/fetch/AAPL/`  
- **Method:** GET  
- **Description:**  
  Fetches financial data for the given symbol and stores it in PostgreSQL.

---

### 4. **Generate PDF Report**  
- **URL:** `http://20.40.45.7:8000/api/report`  
- **Method:** GET  
- **Description:**  
  Generates a PDF performance report based on the financial data and backtesting results.

---

## Installation

Follow the steps below to set up the project on your local machine:

1. **Clone the repository:**  
   ```bash
   git clone <repository-url>
   cd finance_backend

2. **Create a virtual environment:**  
   ```bash
   python3 -m venv .venv

3. **Activate the virtual environment:**
- **On macOS/Linux:**
   - ```bash
     source .venv/bin/activate
- **On Windows:**
   - ```bash
     .venv\Scripts\activate

4. **Install dependencies:**  
   ```bash
   pip install -r requirements.txt

## Testing Endpoint Software
You can use POSTMAN to test it


