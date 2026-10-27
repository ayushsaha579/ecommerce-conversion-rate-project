# E-Commerce Conversion Rate Analytics

A beginner-friendly portfolio project using **Python, Pandas, NumPy, Matplotlib, Streamlit, and MySQL**.

> The included 3,500-session dataset is synthetic demo data, not real customer data.

## Business problem
Understand what proportion of website sessions become purchases and which marketing channels, devices, countries, and landing pages perform best.

## Questions answered
1. What is the overall conversion rate?
2. Which marketing channel converts best?
3. Do conversion rates differ by device?
4. Which landing pages generate the most revenue?
5. How do sessions and conversions change over time?
6. What is the average order value (AOV)?

## Folder structure
```text
ecommerce-conversion-rate-project/
├── app.py
├── requirements.txt
├── data/sessions.csv
├── src/analysis.py
├── sql/schema.sql
└── tests/test_analysis.py
```

## Setup on Windows / VS Code
Open this project folder in VS Code. Choose Terminal → New Terminal and run:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

If `py` is not recognized, use `python -m venv .venv`.

## Run dashboard
Run from the folder containing `app.py` and `requirements.txt`:

```powershell
.\.venv\Scripts\python.exe -m streamlit run app.py
```

Open the local URL Streamlit displays (usually `http://localhost:8501`).

## Run tests
```powershell
.\.venv\Scripts\python.exe -m pytest
```

## Metric definitions
- Conversion rate = converted sessions ÷ total sessions × 100
- Average order value (AOV) = revenue ÷ conversions
- Revenue per session = revenue ÷ sessions

## MySQL
`sql/schema.sql` creates the database and table and provides queries. The dashboard reads the included CSV, so it runs without a MySQL server. For a SQL extension, import the CSV into the MySQL table and run the queries in MySQL Workbench.

## GitHub
`.gitignore` excludes `.venv/`. After creating an empty GitHub repository, run:

```powershell
git init
git add .
git commit -m "Build e-commerce conversion analytics project"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/YOUR-REPO.git
git push -u origin main
```

## Resume description
Built an interactive e-commerce conversion analytics dashboard using Python, Pandas, NumPy, Matplotlib, and Streamlit. Analyzed session-level conversion, revenue, device, channel, and landing-page performance, with filtering and CSV export. Added a MySQL schema and reusable SQL queries.
