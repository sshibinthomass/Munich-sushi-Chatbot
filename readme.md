# End to End Project Agentic AI Chatbots

---

## 1. Clone or Download the Repository
Clone this repository or download it as a ZIP and extract it to your desired location.

```sh
git clone <your-repo-url>
cd <repo-directory>
```

---

## 2. Install Ollama and Add LLM Models

Ollama is required to run local LLMs. Follow these steps:

### 2.1 Download and Install Ollama
- **Windows**: [Download the Windows installer](https://ollama.com/download)
- **macOS**: [Download the macOS installer](https://ollama.com/download)
- **Linux**: Run:
  ```sh
  curl -fsSL https://ollama.com/install.sh | sh
  ```
For more details, visit the [Ollama installation page](https://ollama.com/download).

### 2.2 Start the Ollama Server
After installation, start the Ollama server:
```sh
ollama serve
```

### 2.3 Add/Download an LLM Model
To use a specific LLM (e.g., llama2), pull it using:
```sh
ollama pull llama2
```
Replace `llama2` with the model you want (e.g., `mistral`, `llama3`, etc.).
See available models at the [Ollama models page](https://ollama.com/library).

---

## 3. Set Up Environment Variables

Create a `.env` file in your project root and add the following keys:

```ini
# Ollama server URL (default is local)
OLLAMA_BASE_URL=http://localhost:11434

# Hugging Face API Token
HF_TOKEN=your_huggingface_token_here

# LangChain API Key and Project
LANGCHAIN_API_KEY=your_langchain_api_key_here
LANGCHAIN_PROJECT=your_langchain_project_name_here

# Groq API Key
GROQ_API_KEY=your_groq_api_key_here

# OpenAI API Key
OPENAI_API_KEY=your_openai_api_key_here

# Tavily API Key
TAVILY_API_KEY=your_tavily_api_key_here
```

### How to get these keys
- **OLLAMA_BASE_URL**: If running Ollama locally, use `http://localhost:11434`. For remote servers, use the appropriate URL.
- **HF_TOKEN**: [Create a Hugging Face account](https://huggingface.co/join) and get your token from [https://huggingface.co/settings/tokens](https://huggingface.co/settings/tokens).
- **LANGCHAIN_API_KEY & LANGCHAIN_PROJECT**: [Sign up for LangChain](https://www.langchain.com/) and get your API key and project name from your LangChain dashboard.
- **GROQ_API_KEY**: [Sign up for Groq](https://console.groq.com/keys) and generate an API key.
- **OPENAI_API_KEY**: [Sign up for OpenAI](https://platform.openai.com/signup) and create an API key at [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys). Use this key to access OpenAI models (e.g., GPT-3.5, GPT-4, etc.).
- **TAVILY_API_KEY**: [Sign up for Tavily](https://app.tavily.com/) and get your API key from your account settings.

After creating your `.env` file, the application will automatically load these variables at startup.

---

## 4. Install UV and Project Dependencies

### 4.1 Install [UV](https://github.com/astral-sh/uv) (if not already installed)
UV is a fast Python package manager. Install it by following the [official instructions](https://github.com/astral-sh/uv#installation).

### 4.2 Initialize UV in the project directory
```sh
uv init
```

### 4.3 Create a virtual environment using UV
```sh
uv venv
```

### 4.4 Activate the virtual environment
- **Windows**:
  ```sh
  .venv\Scripts\activate
  ```
- **macOS/Linux**:
  ```sh
  source .venv/bin/activate
  ```

### 4.5 Install dependencies from `requirements.txt`
```sh
uv add -r requirements.txt
```
This will install all required packages listed in `requirements.txt` using UV.

---

## 5. Run the Streamlit App

To start the Streamlit application, run:

```sh
streamlit run app.py
```

This will launch the app in your default web browser. Make sure your virtual environment is activated before running this command.

---

## Summary of Steps
1. Clone/download the repository
2. Install Ollama and add LLM models
3. Set up your `.env` file with required keys
4. Install UV and dependencies, create and activate your virtual environment
5. Run the Streamlit app

Follow these steps in order for a smooth setup and usage experience.
