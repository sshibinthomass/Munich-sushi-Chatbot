# End to End Project Agentic AI Chatbots

---

## 1. Clone or Download the Repository
Clone this repository or download it as a ZIP and extract it to your desired location.

```sh
git clone <your-repo-url>
cd <repo-directory>
```

---

## 2. Set Up Environment Variables

Create a `.env` file in your project root and add the following keys:

```ini
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
- **HF_TOKEN**: [Create a Hugging Face account](https://huggingface.co/join) and get your token from [https://huggingface.co/settings/tokens](https://huggingface.co/settings/tokens).
- **LANGCHAIN_API_KEY & LANGCHAIN_PROJECT**: [Sign up for LangChain](https://www.langchain.com/) and get your API key and project name from your LangChain dashboard.
- **GROQ_API_KEY**: [Sign up for Groq](https://console.groq.com/keys) and generate an API key.
- **OPENAI_API_KEY**: [Sign up for OpenAI](https://platform.openai.com/signup) and create an API key at [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys). Use this key to access OpenAI models (e.g., GPT-3.5, GPT-4, etc.).
- **TAVILY_API_KEY**: [Sign up for Tavily](https://app.tavily.com/) and get your API key from your account settings.

After creating your `.env` file, the application will automatically load these variables at startup.

---

## 3. Install UV and Project Dependencies

### 3.1 Install [UV](https://github.com/astral-sh/uv) (if not already installed)
UV is a fast Python package manager. Install it by following the [official instructions](https://github.com/astral-sh/uv#installation).

### 3.2 Initialize UV in the project directory
```sh
uv init
```

### 3.3 Create a virtual environment using UV
```sh
uv venv
```

### 3.4 Activate the virtual environment
- **Windows**:
  ```sh
  .venv\Scripts\activate
  ```
- **macOS/Linux**:
  ```sh
  source .venv/bin/activate
  ```

### 3.5 Install dependencies from `requirements.txt`
```sh
uv add -r requirements.txt
```
This will install all required packages listed in `requirements.txt` using UV.

### 3.6 Install Node.js Dependencies
Some features require Node.js packages. Install them globally using npm:

```sh
npm install -g @cablate/mcp-google-map
```

---

## 4. Run the Streamlit App

To start the Streamlit application, run:

```sh
streamlit run app.py
```

This will launch the app in your default web browser. Make sure your virtual environment is activated before running this command.

---

## Summary of Steps
1. Clone/download the repository
2. Set up your `.env` file with required keys
3. Install UV and dependencies, create and activate your virtual environment
4. Run the Streamlit app

Follow these steps in order for a smooth setup and usage experience.
