# 🕵️‍♂️ Stylometric AI Text Detector (Rabin–Karp Algorithm)

A pattern-recognition tool designed to identify “artificial” writing styles by analyzing structural repetition and high-frequency n-grams using the **Rabin–Karp Rolling Hash Algorithm**.

> **Course:** Design and Analysis of Algorithms (DAA)
> **Stack:** React.js (Frontend) + Python FastAPI (Backend)

---

## 🧠 The Algorithm: Why Rabin–Karp?

Unlike standard string matching (**O(n × m)**), this project utilizes the **Rabin–Karp algorithm** for efficient multi-pattern search.

1. **Rolling Hash:**
   The system generates hash values for specific “suspicious” phrase windows (trigrams/quadgrams) commonly used by LLMs (e.g., *“delve into,” “tapestry of,” “in conclusion”*).

2. **Pattern Matching:**
   A sliding window moves across the user's text, calculating hashes in **O(1)** time using the rolling hash formula and comparing them against a pre-computed database of AI fingerprints.

3. **Stylometric Scoring:**
   Matches are weighted based on their probability of being “robotic” (e.g., *“delve” = 10 pts, “however” = 2 pts*) to generate a final **AI Likelihood Score**.

---

## 🚀 Tech Stack

* **Frontend:** React + Vite (JavaScript)
* **Styling:** Tailwind CSS
* **Backend:** Python + FastAPI
* **Package Manager:** pnpm (or Bun)

---

## 🛠️ Installation & Setup

### Prerequisites

* Python 3.8+
* Node.js
* **pnpm** or **Bun** installed globally

---

### 1. Clone the Repository

```bash
git clone https://github.com/mirza-mohammad24/ai-text-detector.git
cd ai-text-detector
```

---

### 2. Setup Backend (Python)

Navigate to the backend folder and install dependencies:

```bash
cd backend
python -m venv venv

# Windows:
.\venv\Scripts\activate

# Mac/Linux:
source venv/bin/activate

pip install -r requirements.txt
uvicorn main:app --reload
```

The API will start at:
`http://127.0.0.1:8000`

---

### 3. Setup Frontend (React)

Open a new terminal, navigate to the frontend folder, and start the app.

**Using pnpm:**

```bash
cd frontend
pnpm install
pnpm run dev
```

**Using Bun:**

```bash
cd frontend
bun install
bun run dev
```

The application will start at:
`http://localhost:5173`

---

## 📸 Usage

1. Paste text into the input box.
2. Click **Analyze Text**.
3. View the **AI Likelihood Score** along with highlighted suspicious patterns.

---

## 📄 License

This project is intended for **educational purposes**.
