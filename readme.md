

# 🌍 PlanPal - AI Travel Planner  
**Where Planning Meets Adventure**

**PlanPal** is an AI-powered travel assistant built using **Agentic AI** principles. It helps users generate personalized trip plans based on destination, travel style, budget, and duration. From day-wise itineraries to budget breakdowns and local recommendations — PlanPal takes care of it all!

---

## ✨ Features

- 🌎 Destination-aware, multi-day itinerary planning  
- 💸 Smart budget analysis and money-saving tips  
- 🏨 Personalized accommodation and dining recommendations  
- 🎒 Travel style customization (luxury, backpacking, family, etc.)  
- 📋 Markdown-formatted output with expandable sections  
- ⚙️ Built using LangChain + Ollama + Streamlit  

---

## 🚀 Tech Stack

| Technology     | Purpose                                         |
|----------------|-------------------------------------------------|
| `Python`       | Core programming language                       |
| `Streamlit`    | Frontend UI for user interaction                |
| `LangChain`    | Agent-based orchestration with tool execution   |
| `Ollama`       | Local LLM inference using models like LLaMA3    |

---

## 🛠️ Installation & Setup

### 1. **Clone the repo**

```bash
git clone https://github.com/shenoy-dsouza/plan-pal.git
cd plan-pal
```

### 2. **Create a virtual environment**

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

### 3. **Install dependencies**

```bash
pip install -r requirements.txt
```

---

### 4. 🤖 Set Up Ollama for Local LLM Inference  
> 💡 Prefer an API-based setup? [Click here to use Together AI instead](#-optional-use-together-ai-instead-of-ollama)

PlanPal uses **Ollama** to run large language models like `llama3` **locally** — no OpenAI key required.

### Install Ollama

#### macOS

```bash
brew install ollama
```
Or download the macOS installer from: [https://ollama.com/download](https://ollama.com/download)

#### Windows

1. Download the Windows installer from: [https://ollama.com/download](https://ollama.com/download)  
2. Run the installer and follow the setup instructions.

#### Linux

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

### Pull the required model

```bash
ollama pull llama3
```

> You can use other models as well, like `mistral`, `gemma`, etc.

---

### 5. **Run the app**

```bash
streamlit run app/webapp/planner.py
```

---

## 📸 Screenshots

> *(Add screenshots or GIFs here showing the interface and results)*

---

## 🧠 Behind the Scenes

This app uses **LangChain agents** that dynamically select and invoke tools based on user prompts.  
Powered by Agentic AI design, tools act like smart assistants to get things done.

### Tools used:

- 🗺️ `Itinerary_Planner`: Day-wise trip planning with time slots  
- 💰 `Budget_Analyzer`: Category-wise cost breakdown with savings advice  
- 🏨 `Place_Recommender`: Recommendations for stays and dining based on style & budget  

---

## 💡 Customization Tips

- Add or modify tools inside `app/core/tools.py`  
- Update prompts to suit your use case or language style  
- Customize the UI in `app/webapp/planner.py`  
- Future ideas: Export to PDF, trip sharing link, map integration, etc.

---


## 🧩 Optional: Use Together AI Instead of Ollama

PlanPal also supports **Together AI** as a backend for running **LLaMA-3** or other open models via API.

To use Together AI:

1. Install the Together module:
   ```bash
   pip install -U langchain-together
   ```

2. Add your Together API key to a `.env` file:
   ```
   TOGETHER_API_KEY=your-key-here
   ```
You can get your key from [https://api.together.xyz/settings/keys](https://api.together.xyz/settings/keys)

> 💡 Make sure you're using the `langchain_together` package and importing correctly:


3. Use it in your code:
   ```python
   from langchain_together import Together

   llm = Together(
       model="meta-llama/Llama-3-8b-chat-hf",
       temperature=0.7
   )
   ```

> This allows you to run the app without needing to install Ollama or use local compute.

