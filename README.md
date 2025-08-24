# 🧾 AI Assisted Personal Finance Management System  

A **privacy-first personal finance dashboard** built with **Streamlit**.  
It helps users analyze transactions, visualize spending, run financial simulations, and optionally chat with an **AI assistant** for plain-language insights.  

---

## ✨ Features  

- **📊 Dashboard & Analytics**  
  - Upload transactions (CSV)  
  - Track monthly income vs. expenses  
  - Category breakdowns and recent activity  

- **🦋 Butterfly Effect Simulator**  
  - See long-term effects of small savings changes  
  - Compounding with stochastic market returns  

- **🔮 Financial Scenario Tester**  
  - Monte Carlo simulations for job loss, medical bills, market swings  
  - Probabilities of hitting emergency fund goals  

- **🤖 AI-Powered Assistant** *(optional)*  
  - Ask natural questions about your budget & spending  
  - Example:  
    - “What are my top 3 spending categories in 2024?”  
    - “How much did I spend on groceries vs. restaurants last month?”  
    - “What’s my average monthly savings rate?”  
  - Powered by OpenAI GPT models (`gpt-4o-mini` default)  

---

## 🛠️ Tech Stack  

- **Frontend & App:** [Streamlit](https://streamlit.io/)  
- **Data Analysis:** Pandas, Numpy  
- **Visualization:** Matplotlib  
- **Simulation:** Monte Carlo, Brownian Motion  
- **AI Assistant (optional):** OpenAI API  
- **Deployment:** Docker, Render/Railway/AWS/GCP  

---

## 📂 Project Structure  

```
ai_personal_finance_app/
│
├── app/
│   ├── streamlit_app.py      # Main app
│   ├── data_gen.py           # Generate sample dataset
│   └── modules/
│       ├── simulators.py     # Financial simulations
│       └── llm_bot.py        # AI assistant integration
│
├── data/
│   └── transactions_large.csv   # Sample transactions (~12k rows)
│
├── .env.example              # Example config (copy → .env)
├── requirements.txt          # Dependencies
├── Dockerfile                # For container deployment
└── README.md                 # Project documentation
```

---

## ⚡ Quickstart  

### 1️⃣ Clone & Setup  
```bash
git clone https://github.com/your-username/ai-personal-finance-app.git
cd ai-personal-finance-app
python -m venv .venv
# activate venv
source .venv/Scripts/activate     # Git Bash
# or
.venv\Scripts\activate            # Command Prompt / PowerShell
```

### 2️⃣ Install Requirements  
```bash
pip install -r requirements.txt
```

### 3️⃣ Configure Environment  
```bash
cp .env.example .env
```

Edit `.env`:
```env
OPENAI_API_KEY=sk-xxxxxx        # optional for AI bot
APP_USERNAME=demo               # login username
APP_PASSWORD=MyFinance01@       # login password
```

### 4️⃣ Run App  
```bash
streamlit run app/streamlit_app.py
```
Open 👉 [http://localhost:8501](http://localhost:8501)  

---

## 📤 Using Your Data  

CSV format:
```
date, description, category, amount, type
2024-04-10,Salary payment,Salary,4000,income
2024-04-12,Walmart groceries,Groceries,120.50,expense
2024-04-14,Uber ride,Transport,25.00,expense
```

- `type` = `income` or `expense`  
- Replace with your own transactions or start with the included `transactions_large.csv`.  

---

## 🐳 Docker Deployment  

```bash
docker build -t finance-app .
docker run -p 8501:8501 --env-file .env finance-app
```

---

## ☁️ Cloud Deployment  

- **Render/Railway:** Deploy directly from GitHub (Dockerfile auto-detected).  
- **Google Cloud Run:**  
  ```bash
  gcloud builds submit --tag gcr.io/PROJECT/finance-app
  gcloud run deploy finance-app --image gcr.io/PROJECT/finance-app     --platform managed --allow-unauthenticated     --set-env-vars OPENAI_API_KEY=sk-xxxx,APP_USERNAME=demo,APP_PASSWORD=MyFinance01@
  ```
- **AWS ECS Fargate:** Push Docker image to ECR → create ECS service → expose port 8501.  

---

## ⚠️ Disclaimer  

This project is for **educational and personal use only**.  
It does **not provide financial, tax, or legal advice**.  
Use your own judgment before making financial decisions.  

---

## 📜 License  

MIT License — free to use, modify, and share.  
