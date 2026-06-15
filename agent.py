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
        self.model = "claude-sonnet-4-20250514"  # Using Sonnet 4 as requested

        # Load Air2Energy context
        self.context = self._load_air2energy_context()

    def _load_air2energy_context(self) -> str:
        """Load the Air2Energy brief for context."""
        try:
            with open('/Users/andrewsmithyman/air2energy-tools/AIR2ENERGY_MARKET_BRIEF.md', 'r') as f:
                return f.read()
        except FileNotFoundError:
            return """
            Air2Energy creates retrofit systems that capture CO₂ from gas boiler exhaust and convert it to electricity.

            TARGET CUSTOMERS:
            - Commercial property managers (Westfield, Lendlease)
            - Multi-tenant buildings with gas heating
            - Industrial facilities with gas boilers
            - High Scope 1 emissions from natural gas
            - Sustainability commitments & net zero targets
            - Building Management System (BMS) infrastructure
            - ASRS compliance requirements (Australia)

            SOLUTION: 2.5-8 year payback, 70% margins, retrofit system, no operational disruption

            SCORING CRITERIA:
            - Gas boiler infrastructure (high priority)
            - Scope 1 emissions from natural gas
            - Sustainability investments & commitments
            - Commercial/industrial property portfolio size
            - BMS infrastructure in place
            - Net zero targets and timelines
            """

    def research_company(self, company_name: str) -> Dict[str, Any]:
        """Research a company using web search and Anthropic API."""

        research_prompt = f"""
        You are a market research agent for Air2Energy, a startup that creates retrofit systems to capture CO₂ from gas boiler exhaust and convert it to electricity.

        Research the company "{company_name}" and provide detailed analysis for potential fit with Air2Energy's solution.

        CONTEXT: {self.context}

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

            return {"research_content": response.content}

        except Exception as e:
            print(f"Error during research: {e}")
            return {"research_content": f"Error researching {company_name}: {str(e)}"}

    def score_company_fit(self, company_name: str, research_data: Dict[str, Any]) -> Dict[str, Any]:
        """Score company fit with Air2Energy based on research data."""

        scoring_prompt = f"""
        You are evaluating the company "{company_name}" for fit with Air2Energy's retrofit gas boiler technology.

        COMPANY RESEARCH DATA:
        {research_data.get('research_content', 'No research data available')}

        AIR2ENERGY CONTEXT:
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