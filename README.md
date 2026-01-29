# AI Resume Builder (FastAPI)

An AI-powered resume builder that generates **ATS-optimized resumes** based on a given **Job Description (JD)**.  
The system analyzes job requirements, matches skills, scores resumes, recommends missing skills, and generates resumes in **HTML and PDF formats**.

---

## 🚀 Features

- 📄 Save user profile (skills, education, contact details)
- 📝 Analyze job descriptions and extract required skills
- 🔍 Skill matching between profile and job description
- 📊 Resume scoring based on JD relevance
- 💡 Skill recommendations to improve job fit
- 🧠 Auto-generated resume summary
- 🎨 Resume template selection (ATS-friendly)
- 📄 HTML resume generation
- 📥 PDF resume download using WeasyPrint

---

## 🛠️ Tech Stack

- **Backend:** Python, FastAPI
- **Templating:** Jinja2
- **PDF Generation:** WeasyPrint
- **API Documentation:** Swagger (OpenAPI)
- **Version Control:** Git & GitHub

---

## 📂 Project Structure

resume-ai-builder/
│
├── backend/
│   ├── main.py
│   ├── models/
│   ├── services/
│   ├── templates/
│
├── requirements.txt
├── .gitignore
├── README.md

---

## ⚙️ How to Run Locally

### 1️⃣ Clone the repository
```bash
git clone https://github.com/sharathchandra1110/ai-resume-builder.git
cd ai-resume-builder

2️⃣ Create & activate virtual environment
python3 -m venv venv
source venv/bin/activate
3️⃣ Install dependencies
pip install -r requirements.txt
4️⃣ Run the server
python -m uvicorn backend.main:app --reload
5️⃣ Open API Docs
http://127.0.0.1:8000/docs

📌 Use Case

This project helps:
	•	Students and freshers tailor resumes to job descriptions
	•	Professionals improve ATS scores
	•	Job seekers identify missing skills before applying
🔮 Future Enhancements
	•	Frontend UI (React / Next.js)
	•	Multiple resume templates
	•	Resume upload & optimization
	•	Cloud deployment
	•	Authentication & user accounts

👨‍💻 Author

Sharath Chandra
GitHub: https://github.com/sharathchandra1110
