#!/usr/bin/env python3
"""
Air2Energy Market Research Agent - DEMO MODE

Demonstrates the agent structure and output format without requiring API calls.
Shows example analysis for known companies.
"""

import json
import os
import re
from datetime import datetime
from typing import Dict, Any

# Demo data for known companies
DEMO_COMPANIES = {
    "scentre group": {
        "company_name": "Scentre Group",
        "fit_score": 9.2,
        "overview": "Australia's largest shopping center operator with 42 Westfield destinations",
        "gas_boilers": "YES - Large commercial properties require substantial heating systems",
        "sustainability": "Net zero target 2030, 10,074 tonnes Scope 1 emissions, natural gas main problem",
        "contacts": ["Elliott Rusanow (CEO)", "Andrew Clarke (CFO)", "Sustainability Director"],
        "talking_points": [
            "Direct Scope 1 solution for your main emissions pain point",
            "BMS integration ready across all 42 destinations",
            "8-year payback funds your 2030 net zero journey"
        ],
        "questions": [
            "What's the typical size of gas boilers across your destinations?",
            "How are you managing Scope 1 emissions currently?",
            "What's your approval process for building efficiency investments?"
        ]
    },
    "lendlease": {
        "company_name": "Lendlease",
        "fit_score": 8.7,
        "overview": "Major property developer and manager with global operations",
        "gas_boilers": "YES - Developer/manager of commercial buildings with LNG heating systems",
        "sustainability": "Scope 2 net zero achieved, Scope 1: 2,371 tonnes, LNG emissions key problem",
        "contacts": ["Tony Lombardo (CEO)", "Sustainability Director", "Head of Property Operations"],
        "talking_points": [
            "Complete your net zero journey by solving remaining Scope 1 LNG emissions",
            "Retrofit existing portfolio while integrating into new developments",
            "Operational cost reduction to improve development margins"
        ],
        "questions": [
            "Which buildings in your portfolio still use LNG heating?",
            "What's your timeline for retrofitting existing properties?",
            "How do you evaluate new building efficiency technologies?"
        ]
    },
    "multiplex": {
        "company_name": "Multiplex",
        "fit_score": 7.4,
        "overview": "International construction and property services company",
        "gas_boilers": "LIKELY - Construction company managing commercial properties and projects",
        "sustainability": "Active sustainability focus, renewable energy investments, emission reduction initiatives",
        "contacts": ["Regional Managing Director", "Sustainability Manager", "Project Development Director"],
        "talking_points": [
            "Integrate Air2Energy into your sustainable building portfolio",
            "Offer clients emission reduction + cost savings in new developments",
            "Proven retrofit solution for existing managed properties"
        ],
        "questions": [
            "Do you manage properties post-construction with gas heating?",
            "How do you incorporate sustainability tech into client projects?",
            "What's your experience with building retrofit technologies?"
        ]
    }
}

def demo_research(company_name: str) -> Dict[str, Any]:
    """Generate demo research report for known companies."""

    company_key = company_name.lower().strip()

    if company_key in DEMO_COMPANIES:
        data = DEMO_COMPANIES[company_key]

        return {
            "company_name": data["company_name"],
            "research_date": datetime.now().isoformat(),
            "agent_version": "Air2Energy Market Research Agent v1.0 (DEMO MODE)",
            "fit_score": data["fit_score"],
            "demo_mode": True,
            "research_data": {
                "research_content": f"DEMO DATA for {data['company_name']}"
            },
            "analysis": f"""## COMPANY OVERVIEW
{data['overview']}

## GAS BOILER INFRASTRUCTURE ASSESSMENT
{data['gas_boilers']}

## SUSTAINABILITY COMMITMENTS
{data['sustainability']}

## KEY CONTACTS
{', '.join(data['contacts'])}

## FIT SCORE & REASONING
**Score: {data['fit_score']}/10**

This is demo analysis showing how the agent evaluates companies based on Air2Energy fit criteria.

## TOP 3 TALKING POINTS
{chr(10).join(f"{i+1}. {point}" for i, point in enumerate(data['talking_points']))}

## TOP 3 DISCOVERY QUESTIONS
{chr(10).join(f"{i+1}. {q}" for i, q in enumerate(data['questions']))}
""",
            "air2energy_context_used": True
        }
    else:
        # Generic demo for unknown companies
        return {
            "company_name": company_name,
            "research_date": datetime.now().isoformat(),
            "agent_version": "Air2Energy Market Research Agent v1.0 (DEMO MODE)",
            "fit_score": 5.0,
            "demo_mode": True,
            "research_data": {
                "research_content": f"DEMO MODE - No specific data available for {company_name}"
            },
            "analysis": f"""## COMPANY OVERVIEW
Demo analysis for {company_name} - replace with real Anthropic API research.

## GAS BOILER INFRASTRUCTURE ASSESSMENT
DEMO MODE - Would assess gas heating infrastructure presence

## SUSTAINABILITY COMMITMENTS
DEMO MODE - Would analyze net zero targets and emission reduction initiatives

## KEY CONTACTS
DEMO MODE - Would identify sustainability officers and facility managers

## FIT SCORE & REASONING
**Score: 5.0/10 (Demo Default)**

This is demo mode - real agent uses Anthropic API with web search for accurate analysis.

## TOP 3 TALKING POINTS
1. DEMO - Scope 1 emissions reduction potential
2. DEMO - Operational cost savings through retrofit
3. DEMO - No disruption to existing operations

## TOP 3 DISCOVERY QUESTIONS
1. DEMO - Do you operate buildings with gas heating systems?
2. DEMO - What are your current sustainability commitments?
3. DEMO - How do you evaluate new building efficiency technologies?
""",
            "air2energy_context_used": True
        }

def save_demo_report(report: Dict[str, Any], company_name: str) -> str:
    """Save demo report to JSON file."""

    safe_name = re.sub(r'[^\w\s-]', '', company_name).strip()
    safe_name = re.sub(r'[-\s]+', '_', safe_name)

    filename = f"{safe_name}_air2energy_research_DEMO.json"
    filepath = os.path.join(os.getcwd(), filename)

    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        return filepath
    except Exception as e:
        print(f"Error saving demo report: {e}")
        return ""

def main():
    """Main demo function."""

    print("🎮 Air2Energy Market Research Agent - DEMO MODE")
    print("=" * 55)
    print("This demo shows how the agent works without requiring API keys.")
    print("Available demo companies: Scentre Group, Lendlease, Multiplex")
    print("(You can enter any company name to see the generic demo format)")
    print()

    company_name = input("Enter company name to research: ").strip()

    if not company_name:
        print("❌ Please provide a company name.")
        return

    print(f"\n🔍 Generating demo analysis for {company_name}...")

    # Generate demo report
    report = demo_research(company_name)

    # Save report
    filepath = save_demo_report(report, company_name)

    # Display summary
    print(f"\n✅ Demo Analysis Complete!")
    print(f"📋 Company: {company_name}")
    print(f"⭐ Fit Score: {report['fit_score']}/10")

    if filepath:
        print(f"💾 Demo report saved: {filepath}")

    if report.get('demo_mode'):
        print(f"🎮 This was demo mode - real agent uses Anthropic API for live research")

    # Show key insights
    print(f"\n📈 Demo Analysis Summary:")
    if 'overview' in str(report.get('analysis', '')):
        lines = report['analysis'].split('\n')
        for line in lines[1:4]:  # Show first few lines
            if line.strip():
                print(f"   {line.strip()}")

    print(f"\n🚀 To use real agent:")
    print(f"   1. Get Anthropic API key: https://console.anthropic.com/")
    print(f"   2. Set API key: export ANTHROPIC_API_KEY='your-key'")
    print(f"   3. Run real agent: ./run_agent.sh")

if __name__ == "__main__":
    main()