#!/usr/bin/env python3
"""
Air2Energy Market Research Agent

Analyzes companies for fit with Air2Energy's gas boiler retrofit technology.
Scores companies 1-10 based on sustainability commitments, gas heating infrastructure,
and decarbonisation needs.
"""

import json
import os
import re
from datetime import datetime
from typing import Dict, Any, List

try:
    import anthropic
except ImportError:
    print("Error: anthropic package not installed. Run: pip install anthropic")
    exit(1)

class Air2EnergyMarketAgent:
    def __init__(self, api_key: str = None):
        """Initialize the market research agent."""
        self.api_key = api_key or os.environ.get('ANTHROPIC_API_KEY')
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable not set")

        self.client = anthropic.Anthropic(api_key=self.api_key)
        self.model = "claude-sonnet-4-6"  # Using Sonnet 4 as requested

        # Load Air2Energy context
        self.context = self._load_air2energy_context()

    def _load_air2energy_context(self) -> str:
        """Read context files (AA > BB > CC priority), truncate to fit token budget, then summarise
        into a compact ≤2000-word system prompt via a single Claude call."""
        base = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'context', 'Market reserch')

        source_config = [
            ('AA docs', 'AA — PRIMARY (real customer conversations & internal documents — ground truth)'),
            ('BB docs', 'BB — SECONDARY (reviewed external research — defer to AA on conflicts)'),
            ('CC docs', 'CC — BACKGROUND (basic external research — defer to AA and BB on conflicts)'),
        ]

        # Char budget per tier: keep AA generous, trim CC aggressively (lowest priority)
        tier_char_limits = {'AA docs': 200_000, 'BB docs': 150_000, 'CC docs': 100_000}

        raw_sections = []
        for folder, label in source_config:
            folder_path = os.path.join(base, folder)
            if not os.path.isdir(folder_path):
                continue
            files = sorted(f for f in os.listdir(folder_path) if f.endswith('.md'))
            tier_parts = []
            for filename in files:
                filepath = os.path.join(folder_path, filename)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read().strip()
                    tier_parts.append(f"[{filename}]\n{content}")
                except Exception:
                    pass
            if tier_parts:
                combined = '\n\n'.join(tier_parts)
                limit = tier_char_limits.get(folder, 100_000)
                if len(combined) > limit:
                    combined = combined[:limit] + '\n[... truncated ...]'
                raw_sections.append(f"=== {label} ===\n{combined}")

        if not raw_sections:
            return self._context_fallback()

        print("Summarising context into compact system prompt...")
        return self._summarise_context('\n\n'.join(raw_sections))

    def _summarise_context(self, raw_context: str) -> str:
        """Condense raw prioritised context into a ≤2000-word system prompt via Claude."""
        summarise_prompt = (
            "You are preparing a compact system prompt for an AI market research agent for Air2Energy.\n\n"
            "Air2Energy makes bolt-on electrochemical systems that retrofit onto existing gas boilers, "
            "filter CO₂ from the exhaust, and convert it into electricity fed back into the building. "
            "No fuel change, no operational disruption.\n\n"
            "Below is the full research context split into source tiers.\n"
            "SOURCE PRIORITY: AA (internal docs/real customer conversations) is ground truth. "
            "BB (reviewed external research) is secondary. CC (basic external research) is background only. "
            "When sources conflict, AA overrides BB overrides CC.\n\n"
            f"{raw_context}\n\n"
            "Produce a single compact system prompt of NO MORE THAN 2000 WORDS covering:\n"
            "1. What Air2Energy does and its core value proposition\n"
            "2. Ideal customer profile — industry, infrastructure requirements, pain points\n"
            "3. Key market insights (draw from AA first, supplement with BB and CC)\n"
            "4. Fit scoring criteria: gas boiler infrastructure (30%), portfolio size (25%), "
            "sustainability commitments (20%), tech adoption appetite (15%), decision-maker "
            "accessibility (10%)\n"
            "5. Common objections or challenges surfaced in real customer conversations (AA only)\n"
            "6. Notable named companies or sectors identified as strong targets\n\n"
            "Write as a dense factual briefing — key insights only, no raw data, no tables, no filler. "
            "Open with one sentence stating the AA > BB > CC priority rule."
        )

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=3000,
                messages=[{'role': 'user', 'content': summarise_prompt}]
            )
            summary = response.content[0].text.strip() if response.content else ''
            if summary:
                return summary
        except Exception as e:
            print(f"Warning: context summarisation failed ({e}), using fallback.")

        return self._context_fallback()

    def _context_fallback(self) -> str:
        return (
            "SOURCE PRIORITY: AA (internal docs/customer conversations) overrides BB (reviewed research) "
            "overrides CC (background research).\n\n"
            "Air2Energy creates bolt-on electrochemical systems that retrofit onto existing gas boilers, "
            "filter CO₂ from exhaust, and convert it into electricity fed back into the building. "
            "No fuel change, no operational disruption. 2.5–8 year payback, ~70% margins.\n\n"
            "TARGET CUSTOMERS: Commercial property groups and building owners operating gas boilers at "
            "scale, particularly NABERS-rated buildings still on gas. High Scope 1 emissions from natural "
            "gas, sustainability commitments, net zero targets.\n\n"
            "SCORING: Gas boiler infrastructure (30%), portfolio size (25%), sustainability commitments "
            "(20%), tech adoption appetite (15%), decision-maker accessibility (10%)."
        )

    def research_company(self, company_name: str) -> Dict[str, Any]:
        """Research a company using web search and Anthropic API."""

        research_prompt = f"""
        You are a market research agent for Air2Energy, a startup that creates retrofit systems to capture CO₂ from gas boiler exhaust and convert it to electricity.

        Research the company "{company_name}" and provide detailed analysis for potential fit with Air2Energy's solution.

        CONTEXT (read all sources; when sources conflict, AA overrides BB which overrides CC):
        {self.context}

        Please search the web and provide comprehensive information about:

        1. COMPANY OVERVIEW
        - Business model and primary operations
        - Industry sector and market position
        - Size/scale (number of properties, facilities, employees)
        - Revenue range if available
        - Geographic presence

        2. GAS BOILER INFRASTRUCTURE
        - Do they operate commercial buildings/facilities with gas heating?
        - Any mentions of boiler systems, natural gas usage, or heating infrastructure?
        - Industrial processes that might use gas boilers?
        - Building management or facilities management operations?

        3. SUSTAINABILITY & EMISSIONS
        - Published sustainability commitments or net zero targets
        - Scope 1 emissions data (especially from natural gas)
        - Current decarbonisation initiatives or energy efficiency programs
        - ASRS compliance status (if Australian company)
        - Investment in building management systems (BMS) or smart building tech

        4. KEY CONTACTS & STRUCTURE
        - Sustainability officers, facility managers, or property management executives
        - Corporate structure and decision-making hierarchy
        - Innovation/technology adoption track record

        5. FINANCIAL & STRATEGIC INDICATORS
        - Capital expenditure patterns for building upgrades
        - Partnerships with energy efficiency or sustainability vendors
        - Public commitments around operational cost reduction
        - Environmental, Social, Governance (ESG) reporting

        Search the web thoroughly and provide specific, factual information with sources where possible.
        """

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=4000,
                tools=[{
                    "name": "web_search",
                    "description": "Search the web for information about companies",
                    "input_schema": {
                        "type": "object",
                        "properties": {
                            "query": {"type": "string"}
                        },
                        "required": ["query"]
                    }
                }],
                messages=[{
                    "role": "user",
                    "content": research_prompt
                }]
            )

            # Convert TextBlock objects to string for JSON serialization
            content = str(response.content[0].text) if response.content else "No research data available"
            return {"research_content": content}

        except Exception as e:
            print(f"Error during research: {e}")
            return {"research_content": f"Error researching {company_name}: {str(e)}"}

    def score_company_fit(self, company_name: str, research_data: Dict[str, Any]) -> Dict[str, Any]:
        """Score company fit with Air2Energy based on research data."""

        scoring_prompt = f"""
        You are evaluating the company "{company_name}" for fit with Air2Energy's retrofit gas boiler technology.

        COMPANY RESEARCH DATA:
        {research_data.get('research_content', 'No research data available')}

        AIR2ENERGY CONTEXT (AA = ground truth, BB = secondary, CC = background; AA overrides BB overrides CC on any conflict):
        {self.context}

        Based on this research, provide a comprehensive analysis with the following structure:

        ## COMPANY OVERVIEW
        Brief 2-3 sentence summary of the company and what they do.

        ## GAS BOILER INFRASTRUCTURE ASSESSMENT
        - Do they likely use gas boilers? (Yes/No/Unknown and reasoning)
        - Specific evidence of gas heating systems, commercial properties, or industrial facilities
        - Scale of potential boiler infrastructure (number of properties/facilities)

        ## SUSTAINABILITY COMMITMENTS
        - Net zero targets and timelines
        - Specific Scope 1 emission reduction goals
        - Current sustainability initiatives and investments
        - ASRS compliance needs (if Australian)
        - Track record of adopting new efficiency technologies

        ## KEY CONTACTS
        List 3-5 specific individuals who would be decision makers:
        - Name, Title, and why they're relevant to Air2Energy sales
        - Focus on: sustainability officers, facility managers, property management VPs, innovation directors

        ## FIT SCORE & REASONING
        Score 1-10 where:
        - 9-10: Perfect fit - Large commercial portfolio with gas boilers, strong sustainability commitments, proven tech adoption
        - 7-8: Strong fit - Good portfolio size, some sustainability initiatives, likely gas heating infrastructure
        - 5-6: Medium fit - Some relevant characteristics but missing key criteria
        - 3-4: Weak fit - Limited commercial properties or sustainability focus
        - 1-2: Poor fit - No gas infrastructure, no sustainability commitments, wrong industry

        SCORING FACTORS (weight each):
        - Gas boiler infrastructure presence (30%)
        - Commercial/industrial property portfolio size (25%)
        - Sustainability commitments & net zero targets (20%)
        - Investment appetite for efficiency tech (15%)
        - Decision-maker accessibility (10%)

        Provide specific score and 2-3 sentence reasoning.

        ## TOP 3 TALKING POINTS
        For initial sales outreach, what are the most compelling value propositions for this specific company?
        Format: "Point: Reasoning based on their specific situation"

        ## TOP 3 DISCOVERY QUESTIONS
        Most important questions to ask this company to qualify them further.
        Format: "Question: Why this matters for Air2Energy fit"

        Provide detailed, specific analysis based on the actual research data found.
        """

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=3000,
                messages=[{
                    "role": "user",
                    "content": scoring_prompt
                }]
            )

            # Extract structured data from response
            content = str(response.content[0].text) if response.content else "No analysis generated"

            # Parse the fit score from the content
            score_match = re.search(r'(?:SCORE|Score)[:\s]*(\d+(?:\.\d+)?)', content, re.IGNORECASE)
            fit_score = float(score_match.group(1)) if score_match else 5.0

            return {
                "fit_score": fit_score,
                "analysis": content,
                "timestamp": datetime.now().isoformat()
            }

        except Exception as e:
            print(f"Error during scoring: {e}")
            return {
                "fit_score": 0,
                "analysis": f"Error analyzing {company_name}: {str(e)}",
                "timestamp": datetime.now().isoformat()
            }

    def generate_report(self, company_name: str) -> Dict[str, Any]:
        """Generate complete market research report for a company."""

        print(f"🔍 Researching {company_name}...")

        # Step 1: Research the company
        research_data = self.research_company(company_name)

        print(f"📊 Scoring fit with Air2Energy...")

        # Step 2: Score the company
        scoring_data = self.score_company_fit(company_name, research_data)

        # Step 3: Compile final report
        report = {
            "company_name": company_name,
            "research_date": datetime.now().isoformat(),
            "agent_version": "Air2Energy Market Research Agent v1.0",
            "fit_score": scoring_data["fit_score"],
            "research_data": research_data,
            "analysis": scoring_data["analysis"],
            "air2energy_context_used": True
        }

        return report

    def save_report(self, report: Dict[str, Any], company_name: str) -> str:
        """Save report to JSON file named after the company."""

        # Clean company name for filename
        safe_name = re.sub(r'[^\w\s-]', '', company_name).strip()
        safe_name = re.sub(r'[-\s]+', '_', safe_name)

        filename = f"{safe_name}_air2energy_research.json"
        filepath = os.path.join(os.getcwd(), filename)

        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)

            return filepath

        except Exception as e:
            print(f"Error saving report: {e}")
            return ""

def main():
    """Main function to run the market research agent."""

    print("🚀 Air2Energy Market Research Agent")
    print("=" * 50)

    # Get company name from user
    company_name = input("\nEnter company name to research: ").strip()

    if not company_name:
        print("❌ Please provide a company name.")
        return

    try:
        # Initialize agent
        agent = Air2EnergyMarketAgent()

        # Generate report
        report = agent.generate_report(company_name)

        # Save report
        filepath = agent.save_report(report, company_name)

        # Display summary
        print(f"\n✅ Research Complete!")
        print(f"📋 Company: {company_name}")
        print(f"⭐ Fit Score: {report['fit_score']}/10")

        if filepath:
            print(f"💾 Report saved: {filepath}")

        # Display key insights
        if report.get('analysis'):
            print(f"\n📈 Quick Summary:")
            analysis = report['analysis']

            # Extract overview if available
            overview_match = re.search(r'## COMPANY OVERVIEW\n(.*?)(?=##|\Z)', analysis, re.DOTALL)
            if overview_match:
                overview = overview_match.group(1).strip()[:200]
                print(f"Overview: {overview}...")

            # Extract score reasoning if available
            score_match = re.search(r'## FIT SCORE.*?\n(.*?)(?=##|\Z)', analysis, re.DOTALL)
            if score_match:
                score_reasoning = score_match.group(1).strip()[:300]
                print(f"Fit Reasoning: {score_reasoning}...")

    except ValueError as e:
        print(f"❌ Configuration Error: {e}")
        print("💡 Set your ANTHROPIC_API_KEY environment variable")

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()