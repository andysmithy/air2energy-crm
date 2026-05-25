# Air2Energy CRM

Single-file sales CRM for Air2Energy — contacts, competitor intel, and an AI research agent powered by Claude.

## Setup

**1. Install dependencies**

```bash
cd ~/air2energy-tools
npm install
```

**2. Add your Anthropic API key**

```bash
cp .env.example .env
```

Edit `.env` and replace `sk-ant-your-key-here` with your real key:

```
ANTHROPIC_API_KEY=sk-ant-...
```

**3. Start the proxy server**

```bash
node server.js
```

The proxy runs on `http://localhost:3000` and forwards requests to the Anthropic API server-side, so your API key is never exposed in the browser.

**4. Open the app**

In a second terminal:

```bash
python3 -m http.server 8000
```

Then open `http://localhost:8000` in your browser.

## How it works

```
Browser (localhost:8000)
  └─ POST /v1/messages
       └─ Proxy (localhost:3000)
            └─ adds x-api-key from .env
                 └─ Anthropic API
```

## Files

| File | Description |
|------|-------------|
| `index.html` | The entire app (HTML + CSS + JS, no build step) |
| `server.js` | Node.js proxy that holds the API key server-side |
| `.env` | Your API key — never committed to git |
| `.env.example` | Template for `.env` |
| `context/` | Source documents used to train the research agent system prompt |
