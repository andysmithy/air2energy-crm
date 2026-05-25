# Air2Energy CRM

Single-file sales CRM for Air2Energy — contacts, competitor intel, and an AI research agent powered by Claude.

## Running locally

The research agent calls the Anthropic API directly from the browser. This requires serving the file over HTTP (not opening it as a `file://` URL).

**1. Start a local server**

```bash
cd ~/air2energy-tools
python3 -m http.server 8000
```

**2. Open in your browser**

```
http://localhost:8000
```

**3. Add your Anthropic API key**

Go to the **Research** tab and paste your `sk-ant-…` key. It is saved in your browser's localStorage and never leaves your machine.

## Files

- `index.html` — the entire app (HTML + CSS + JS, no build step)
- `context/` — source documents used to train the research agent system prompt
