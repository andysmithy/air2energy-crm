# Air2Energy Market Research Agent

Automated market research agent that analyzes companies for fit with Air2Energy's gas boiler retrofit technology. Provides scoring (1-10), detailed analysis, and structured sales intelligence.

## Quick Start

**Option 1: Automated Setup**
```bash
./setup.sh                    # One-time setup
export ANTHROPIC_API_KEY="your-key-here"
./run_agent.sh               # Run the agent
```

**Option 2: Manual Setup**
1. **Create virtual environment:**
```bash
python3 -m venv air2energy_env
source air2energy_env/bin/activate
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Set API key:**
```bash
export ANTHROPIC_API_KEY="your-anthropic-api-key-here"
```

4. **Run the agent:**
```bash
python agent.py
```

## Demo Mode (No API Key Required)

Try the demo first to see how the agent works:
```bash
python3 demo_agent.py
```

Demo companies with pre-built analysis:
- **Scentre Group** (Score: 9.2/10)
- **Lendlease** (Score: 8.7/10) 
- **Multiplex** (Score: 7.4/10)

## Get Your API Key

For live research with web search:
1. Sign up at [Anthropic Console](https://console.anthropic.com/)
2. Create a new API key
3. Set it in your environment: `export ANTHROPIC_API_KEY="sk-ant-..."`

## How It Works

1. **Input:** Company name
2. **Research:** Uses Anthropic API with web search to gather:
   - Company overview & business model
   - Gas boiler infrastructure presence
   - Sustainability commitments & emissions data
   - Key decision makers & contacts
   
3. **Scoring:** Evaluates fit on 1-10 scale based on:
   - Gas boiler infrastructure (30% weight)
   - Property portfolio size (25% weight)
   - Sustainability commitments (20% weight)
   - Tech adoption appetite (15% weight)
   - Decision maker accessibility (10% weight)

4. **Output:** Structured JSON report with:
   - Company overview
   - Gas boiler assessment (Yes/No/Unknown)
   - Sustainability commitments analysis
   - Key contacts list
   - Fit score with reasoning
   - Top 3 talking points for sales
   - Top 3 discovery questions

## Scoring Guide

- **9-10 (Perfect Fit):** Large commercial portfolio, confirmed gas boilers, strong sustainability commitments, proven tech adoption
- **7-8 (Strong Fit):** Good portfolio size, likely gas infrastructure, some sustainability initiatives
- **5-6 (Medium Fit):** Some relevant characteristics but missing key criteria
- **3-4 (Weak Fit):** Limited commercial properties or sustainability focus  
- **1-2 (Poor Fit):** No gas infrastructure, wrong industry, no sustainability commitments

## Target Customer Profile

Air2Energy's ideal customers:
- **Westfield/Scentre Group type:** 40+ commercial properties, gas boilers, Scope 1 emissions, net zero targets
- **Lendlease type:** Major developer, sustainability investments, LNG reduction goals
- **Commercial property managers, hospitality, industrial facilities**
- **Building Management Systems (BMS) infrastructure**
- **ASRS compliance requirements (Australian companies)**

## Output Files

Reports saved as: `{Company_Name}_air2energy_research.json`

Example: `Westfield_air2energy_research.json`

## Example Usage

```bash
python agent.py
# Enter company name to research: Scentre Group
# 🔍 Researching Scentre Group...
# 📊 Scoring fit with Air2Energy...
# ✅ Research Complete!
# ⭐ Fit Score: 9.2/10
# 💾 Report saved: Scentre_Group_air2energy_research.json
```

## Use Cases

1. **Lead qualification:** Score inbound leads for sales priority
2. **Market research:** Identify high-potential prospects in target sectors
3. **Competitive analysis:** Research customers of competing solutions
4. **Sales preparation:** Generate talking points & discovery questions before calls
5. **Territory planning:** Map and prioritize accounts by fit score

## Customization

Edit the scoring criteria weights in `score_company_fit()` method:
- Adjust weighting percentages based on sales learnings
- Add new scoring factors (e.g., geographic presence, company size)
- Modify talking points format for specific use cases

## Troubleshooting

- **API Key Error:** Ensure ANTHROPIC_API_KEY is set in environment
- **Web Search Issues:** Agent uses Claude's web search - internet connection required
- **Missing Context:** Agent loads Air2Energy brief from `AIR2ENERGY_MARKET_BRIEF.md`

## Next Steps

After generating reports:
1. Sort companies by fit score for prioritization
2. Use talking points for personalized outreach
3. Prepare discovery questions for qualification calls
4. Track outcomes to improve scoring algorithm