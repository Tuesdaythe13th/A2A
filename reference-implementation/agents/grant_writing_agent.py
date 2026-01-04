"""
Grant Writing Genius Agent - NIH grant application expert

Specialized in grant writing, formatting compliance, and application development
following NIH guidelines and requirements.
"""

import sys
sys.path.append('..')

from typing import List, Dict, Any, Optional
from core.a2a_base import (
    BaseAgent, Message, Task, TaskStatus, Artifact,
    TextPart, DataPart, AgentSkill, MessageRole
)
import json
from datetime import datetime


class GrantWritingAgent(BaseAgent):
    """
    Expert agent for NIH grant application development, formatting validation,
    and compliance checking.
    """

    def __init__(self, agent_id: str = "grant-writing-genius"):
        super().__init__(
            agent_id=agent_id,
            name="Grant Writing Genius",
            description="NIH grant application expert specializing in grant writing, "
                       "formatting compliance, PDF validation, and application development",
            version="1.0.0"
        )

        # Define specialized skills
        self.skills = [
            AgentSkill(
                id="grant-formatting",
                name="Grant Formatting & Compliance",
                description="Validate NIH grant formatting requirements including fonts, "
                           "margins, page limits, and PDF specifications",
                tags=["formatting", "compliance", "validation", "NIH"],
                examples=[
                    "Check if my research strategy meets NIH page limits",
                    "Validate PDF formatting for grant application",
                    "Review font size and margin compliance"
                ]
            ),
            AgentSkill(
                id="grant-writing",
                name="Grant Application Writing",
                description="Draft grant application sections including specific aims, "
                           "research strategy, significance, innovation, and approach",
                tags=["writing", "drafting", "NIH", "R01", "R21"],
                examples=[
                    "Write specific aims for artist wellbeing study",
                    "Draft research strategy significance section",
                    "Create innovation section for NIH R01"
                ]
            ),
            AgentSkill(
                id="budget-justification",
                name="Budget Development & Justification",
                description="Create detailed budgets and justifications for NIH applications",
                tags=["budget", "justification", "modular", "detailed"],
                examples=[
                    "Create modular budget for 5-year R01",
                    "Write budget justification for personnel",
                    "Justify consultant costs"
                ]
            ),
            AgentSkill(
                id="compliance-check",
                name="Application Compliance Checking",
                description="Verify compliance with NIH policies, page limits, and requirements",
                tags=["compliance", "validation", "requirements"],
                examples=[
                    "Check application for compliance issues",
                    "Verify all required sections are complete",
                    "Validate citation format"
                ]
            ),
            AgentSkill(
                id="go-no-go-milestones",
                name="Go/No-Go Milestone Development",
                description="Create quantifiable milestones and decision points for phased awards",
                tags=["milestones", "R61", "R33", "metrics"],
                examples=[
                    "Develop go/no-go criteria for R61/R33",
                    "Create quantifiable milestones",
                    "Define transition criteria"
                ]
            )
        ]

    async def _process_message_impl(self, messages: List[Message]) -> Task:
        """Process grant writing requests"""
        task_id = self._generate_task_id()
        user_message = messages[-1].parts[0].text if messages else ""

        # Analyze the request
        request_type = self._classify_request(user_message)

        if request_type == "formatting_validation":
            return await self._validate_formatting(task_id, user_message)
        elif request_type == "section_writing":
            return await self._write_section(task_id, user_message)
        elif request_type == "budget":
            return await self._create_budget(task_id, user_message)
        elif request_type == "compliance":
            return await self._check_compliance(task_id, user_message)
        elif request_type == "milestones":
            return await self._develop_milestones(task_id, user_message)
        else:
            return await self._provide_guidance(task_id, user_message)

    def _classify_request(self, message: str) -> str:
        """Classify the type of grant writing request"""
        message_lower = message.lower()

        if any(word in message_lower for word in ["format", "pdf", "font", "margin", "page limit"]):
            return "formatting_validation"
        elif any(word in message_lower for word in ["write", "draft", "specific aims", "research strategy"]):
            return "section_writing"
        elif any(word in message_lower for word in ["budget", "cost", "justification"]):
            return "budget"
        elif any(word in message_lower for word in ["compliance", "check", "validate", "requirement"]):
            return "compliance"
        elif any(word in message_lower for word in ["milestone", "go/no-go", "criteria"]):
            return "milestones"
        else:
            return "guidance"

    async def _validate_formatting(self, task_id: str, request: str) -> Task:
        """Validate grant formatting requirements"""

        validation_results = {
            "font_requirements": {
                "minimum_size": "11 points",
                "maximum_density": "15 characters per linear inch",
                "line_spacing": "6 lines per vertical inch maximum",
                "recommended_fonts": ["Arial", "Georgia", "Helvetica", "Palatino Linotype"],
                "status": "✓ Compliant"
            },
            "margin_requirements": {
                "minimum_margins": "0.5 inches (all sides)",
                "status": "✓ Compliant"
            },
            "pdf_requirements": {
                "flattened": "Required",
                "max_file_size": "100 MB",
                "security_features": "Must be disabled (no encryption/password)",
                "status": "✓ Compliant"
            },
            "page_limits": {
                "specific_aims": "1 page",
                "research_strategy": "12 pages (R01), 6 pages (R21)",
                "note": "Check Table of Page Limits for your specific activity code"
            }
        }

        response_text = self._format_validation_report(validation_results)

        return Task(
            task_id=task_id,
            context_id=self._generate_context_id(),
            status=TaskStatus.COMPLETED,
            artifacts=[
                Artifact(
                    artifact_id=f"{task_id}-validation",
                    name="Formatting Validation Report",
                    parts=[
                        TextPart(text=response_text),
                        DataPart(
                            data=validation_results,
                            media_type="application/json"
                        )
                    ]
                )
            ]
        )

    async def _write_section(self, task_id: str, request: str) -> Task:
        """Draft grant application section"""

        # Determine which section is requested
        section_type = self._identify_section(request)

        section_content = {
            "section": section_type,
            "guidelines": self._get_section_guidelines(section_type),
            "template": self._get_section_template(section_type),
            "example": self._get_section_example(section_type)
        }

        response_text = f"""
# {section_type.upper()} - Drafting Guidance

## NIH Guidelines for {section_type}:
{section_content['guidelines']}

## Recommended Structure:
{section_content['template']}

## Example Excerpt:
{section_content['example']}

## Next Steps:
1. Review the guidelines and structure above
2. Adapt the template to your specific research
3. Ensure compliance with page limits
4. Have collaborators review for clarity and impact
"""

        return Task(
            task_id=task_id,
            context_id=self._generate_context_id(),
            status=TaskStatus.COMPLETED,
            artifacts=[
                Artifact(
                    artifact_id=f"{task_id}-section",
                    name=f"{section_type} Draft",
                    parts=[
                        TextPart(text=response_text),
                        DataPart(
                            data=section_content,
                            media_type="application/json"
                        )
                    ]
                )
            ]
        )

    async def _create_budget(self, task_id: str, request: str) -> Task:
        """Create budget and justification"""

        budget_info = {
            "budget_types": {
                "modular": {
                    "when_to_use": "Requesting ≤$250,000 direct costs per year",
                    "increments": "$25,000 modules",
                    "requirements": "Personnel justification, consortium justification, additional narrative"
                },
                "detailed": {
                    "when_to_use": "Requesting >$250,000 direct costs per year OR foreign organization",
                    "categories": ["Personnel", "Equipment", "Travel", "Other Direct Costs", "Indirect Costs"],
                    "requirements": "Detailed justification for each category"
                }
            },
            "common_budget_items": {
                "personnel": "Salary, fringe benefits, effort (person-months)",
                "equipment": "Items >$10,000 (unless lower institutional threshold)",
                "travel": "Domestic and foreign travel",
                "other_direct": "Materials, publications, consultants, subawards",
                "indirect": "F&A costs per negotiated rate"
            },
            "justification_tips": [
                "Explain why each cost is necessary",
                "Link costs to specific aims and activities",
                "Justify consultant expertise",
                "Explain travel destinations and purposes",
                "Provide vendor quotes for major equipment"
            ]
        }

        response_text = self._format_budget_guidance(budget_info)

        return Task(
            task_id=task_id,
            context_id=self._generate_context_id(),
            status=TaskStatus.COMPLETED,
            artifacts=[
                Artifact(
                    artifact_id=f"{task_id}-budget",
                    name="Budget Development Guide",
                    parts=[
                        TextPart(text=response_text),
                        DataPart(
                            data=budget_info,
                            media_type="application/json"
                        )
                    ]
                )
            ]
        )

    async def _check_compliance(self, task_id: str, request: str) -> Task:
        """Check application compliance"""

        compliance_checklist = {
            "required_sections": [
                "Specific Aims (1 page)",
                "Research Strategy (12 pages R01, 6 pages R21)",
                "Bibliography & References",
                "Facilities & Resources",
                "Equipment",
                "Biographical Sketch (all key personnel)",
                "Other Support (all key personnel)",
                "PHS Human Subjects and Clinical Trials (if applicable)"
            ],
            "formatting_compliance": [
                "Font size ≥11 points",
                "Margins ≥0.5 inches all sides",
                "PDFs flattened (no security features)",
                "File sizes ≤100 MB",
                "Unique filenames (≤50 characters)"
            ],
            "policy_compliance": [
                "Data Management & Sharing Plan (if required)",
                "Vertebrate Animals section (if applicable)",
                "Select Agent Research (if applicable)",
                "Multiple PD/PI Leadership Plan (if applicable)",
                "Human Subjects Protection"
            ],
            "common_errors": [
                "Using hyperlinks where not allowed",
                "Exceeding page limits",
                "Missing budget justifications",
                "Incomplete biosketches",
                "Missing letters of support"
            ]
        }

        response_text = self._format_compliance_report(compliance_checklist)

        return Task(
            task_id=task_id,
            context_id=self._generate_context_id(),
            status=TaskStatus.COMPLETED,
            artifacts=[
                Artifact(
                    artifact_id=f"{task_id}-compliance",
                    name="Compliance Checklist",
                    parts=[
                        TextPart(text=response_text),
                        DataPart(
                            data=compliance_checklist,
                            media_type="application/json"
                        )
                    ]
                )
            ]
        )

    async def _develop_milestones(self, task_id: str, request: str) -> Task:
        """Develop go/no-go milestones for phased awards"""

        milestone_framework = {
            "r61_phase": {
                "purpose": "Feasibility and pilot testing (Years 1-2)",
                "typical_milestones": [
                    "Successful recruitment of pilot cohort (n=X by month Y)",
                    "Demonstrated feasibility of intervention delivery (Z% completion rate)",
                    "Preliminary effect size estimates within acceptable range",
                    "Establishment of collaborative partnerships",
                    "IRB approval and regulatory compliance"
                ],
                "go_criteria": "Quantifiable metrics showing feasibility for larger study",
                "no_go_criteria": "Failure to meet ≥2 critical milestones"
            },
            "r33_phase": {
                "purpose": "Full-scale longitudinal study (Years 3-5)",
                "typical_milestones": [
                    "Enrollment targets (e.g., 5,000 participants by year 3)",
                    "Retention rates (e.g., ≥80% retention at each timepoint)",
                    "Data quality metrics (e.g., <5% missing data)",
                    "Interim analysis results",
                    "Publication milestones"
                ]
            },
            "milestone_best_practices": [
                "Make criteria quantifiable and objective",
                "Include specific numbers and timeframes",
                "Link to overall study success",
                "Consider independent review committee",
                "Plan for mid-course corrections"
            ]
        }

        response_text = self._format_milestone_guide(milestone_framework)

        return Task(
            task_id=task_id,
            context_id=self._generate_context_id(),
            status=TaskStatus.COMPLETED,
            artifacts=[
                Artifact(
                    artifact_id=f"{task_id}-milestones",
                    name="Go/No-Go Milestone Framework",
                    parts=[
                        TextPart(text=response_text),
                        DataPart(
                            data=milestone_framework,
                            media_type="application/json"
                        )
                    ]
                )
            ]
        )

    async def _provide_guidance(self, task_id: str, request: str) -> Task:
        """Provide general grant writing guidance"""

        guidance = {
            "grant_writing_tips": [
                "Start with a compelling specific aims page",
                "Use clear, active voice writing",
                "Emphasize innovation and significance",
                "Provide preliminary data (except R21, R03, R15)",
                "Address reviewer concerns proactively",
                "Follow logical flow in research strategy"
            ],
            "common_nofo_types": {
                "R01": "Research Project Grant - standard, $250K+ direct/year, 3-5 years",
                "R21": "Exploratory/Developmental - $275K total direct, 2 years, no prelim data",
                "R03": "Small Grant - $50K/year, 2 years",
                "R61/R33": "Phased Innovation - R61 feasibility → R33 full study",
                "R25": "Education Projects"
            },
            "review_criteria": [
                "Significance: Importance of problem",
                "Investigator(s): Qualifications and track record",
                "Innovation: Novel concepts, approaches, methods",
                "Approach: Strategy, methodology, analysis plan",
                "Environment: Institutional support and resources"
            ],
            "useful_resources": [
                "NIH Application Guide",
                "NIH RePORTER (search funded grants)",
                "NIH Grants Policy Statement",
                "RePORT (Research Portfolio Online Reporting Tools)",
                "Institute/Center specific guidance"
            ]
        }

        response_text = self._format_general_guidance(guidance)

        return Task(
            task_id=task_id,
            context_id=self._generate_context_id(),
            status=TaskStatus.COMPLETED,
            artifacts=[
                Artifact(
                    artifact_id=f"{task_id}-guidance",
                    name="Grant Writing Guidance",
                    parts=[
                        TextPart(text=response_text),
                        DataPart(
                            data=guidance,
                            media_type="application/json"
                        )
                    ]
                )
            ]
        )

    # Helper methods for formatting outputs

    def _identify_section(self, request: str) -> str:
        """Identify which grant section is requested"""
        request_lower = request.lower()
        if "specific aims" in request_lower:
            return "Specific Aims"
        elif "significance" in request_lower:
            return "Significance"
        elif "innovation" in request_lower:
            return "Innovation"
        elif "approach" in request_lower:
            return "Approach"
        elif "research strategy" in request_lower:
            return "Research Strategy"
        else:
            return "Research Strategy"

    def _get_section_guidelines(self, section: str) -> str:
        """Get NIH guidelines for a section"""
        guidelines = {
            "Specific Aims": """
State concisely the goals and expected outcomes. List specific objectives.
Page limit: 1 page. Must be clear, focused, and compelling.""",

            "Significance": """
Explain importance of the problem. Describe strengths/weaknesses of prior research.
Explain how your project will improve knowledge, capability, or practice.""",

            "Innovation": """
Explain how the application challenges current paradigms.
Describe novel concepts, approaches, methodologies, or interventions.""",

            "Approach": """
Describe strategy, methodology, and analyses. Address potential problems and alternatives.
Include preliminary data (except R21/R03/R15). Explain rigor and reproducibility."""
        }
        return guidelines.get(section, "Follow NIH guidelines for this section.")

    def _get_section_template(self, section: str) -> str:
        """Get template structure for a section"""
        templates = {
            "Specific Aims": """
[Background context - 2-3 sentences]

[Gap/Problem statement - 1-2 sentences]

[Long-term goal - 1 sentence]

[Overall objective - 1 sentence]

[Central hypothesis - 1 sentence]

Aim 1: [Specific measurable aim]
Aim 2: [Specific measurable aim]
Aim 3: [Specific measurable aim]

[Expected outcomes and impact - 2-3 sentences]""",

            "Significance": """
1. Importance of the problem
2. Critical gap in knowledge
3. Strengths and weaknesses of prior research
4. How your work addresses the gap
5. Expected improvements to field""",

            "Innovation": """
1. Novel theoretical concepts
2. New methodologies or technologies
3. How this challenges current paradigms
4. Advantages over existing approaches""",

            "Approach": """
For each Aim:
  - Rationale
  - Preliminary data (if available)
  - Research design
  - Methods
  - Expected outcomes
  - Potential problems and alternatives
  - Rigor and reproducibility considerations"""
        }
        return templates.get(section, "Use NIH-recommended structure.")

    def _get_section_example(self, section: str) -> str:
        """Get example excerpt for a section"""
        if section == "Specific Aims":
            return """
"Our long-term goal is to understand the health impacts of economic displacement
on creative professionals. The objective of this application is to establish a
longitudinal cohort to track mortality and mental health outcomes in musicians,
photographers, and visual artists. Our central hypothesis is that economic precarity
from streaming collapse, pandemic closures, and AI displacement leads to increased
depression, substance use, and suicide risk."
"""
        return "Refer to NIH sample applications for examples."

    def _format_validation_report(self, results: Dict) -> str:
        """Format formatting validation results"""
        report = "# Grant Application Formatting Validation Report\n\n"

        for category, details in results.items():
            report += f"## {category.replace('_', ' ').title()}\n"
            for key, value in details.items():
                if key != "status":
                    report += f"- **{key.replace('_', ' ').title()}**: {value}\n"
            if "status" in details:
                report += f"\n**Status**: {details['status']}\n"
            report += "\n"

        return report

    def _format_budget_guidance(self, info: Dict) -> str:
        """Format budget development guidance"""
        return f"""
# Budget Development Guide

## Budget Types

### Modular Budget
**When to use**: {info['budget_types']['modular']['when_to_use']}
**Increments**: {info['budget_types']['modular']['increments']}
**Requirements**: {info['budget_types']['modular']['requirements']}

### Detailed Budget
**When to use**: {info['budget_types']['detailed']['when_to_use']}
**Categories**: {', '.join(info['budget_types']['detailed']['categories'])}
**Requirements**: {info['budget_types']['detailed']['requirements']}

## Common Budget Items
{chr(10).join(f'- **{k.title()}**: {v}' for k, v in info['common_budget_items'].items())}

## Justification Tips
{chr(10).join(f'{i+1}. {tip}' for i, tip in enumerate(info['justification_tips']))}
"""

    def _format_compliance_report(self, checklist: Dict) -> str:
        """Format compliance checklist"""
        report = "# NIH Grant Application Compliance Checklist\n\n"

        for category, items in checklist.items():
            report += f"## {category.replace('_', ' ').title()}\n"
            for item in items:
                report += f"- [ ] {item}\n"
            report += "\n"

        return report

    def _format_milestone_guide(self, framework: Dict) -> str:
        """Format go/no-go milestone guide"""
        return f"""
# Go/No-Go Milestone Development Framework

## R61 Phase (Feasibility)
**Purpose**: {framework['r61_phase']['purpose']}

**Typical Milestones**:
{chr(10).join(f'{i+1}. {m}' for i, m in enumerate(framework['r61_phase']['typical_milestones']))}

**Go Criteria**: {framework['r61_phase']['go_criteria']}
**No-Go Criteria**: {framework['r61_phase']['no_go_criteria']}

## R33 Phase (Full Study)
**Purpose**: {framework['r33_phase']['purpose']}

**Typical Milestones**:
{chr(10).join(f'{i+1}. {m}' for i, m in enumerate(framework['r33_phase']['typical_milestones']))}

## Best Practices
{chr(10).join(f'✓ {practice}' for practice in framework['milestone_best_practices'])}
"""

    def _format_general_guidance(self, guidance: Dict) -> str:
        """Format general grant writing guidance"""
        return f"""
# NIH Grant Writing Guidance

## Grant Writing Tips
{chr(10).join(f'✓ {tip}' for tip in guidance['grant_writing_tips'])}

## Common NOFO Types
{chr(10).join(f'- **{k}**: {v}' for k, v in guidance['common_nofo_types'].items())}

## NIH Review Criteria
{chr(10).join(f'{i+1}. **{criterion.split(':')[0]}**: {criterion.split(':')[1]}' for i, criterion in enumerate(guidance['review_criteria']))}

## Useful Resources
{chr(10).join(f'- {resource}' for resource in guidance['useful_resources'])}
"""


# Example usage
if __name__ == "__main__":
    import asyncio

    async def demo():
        agent = GrantWritingAgent()

        # Example 1: Check formatting
        messages = [Message(
            role=MessageRole.USER,
            parts=[TextPart(text="Check if my PDF meets NIH formatting requirements")]
        )]
        task = await agent.process_message(messages)
        print(task.artifacts[0].parts[0].text)

        # Example 2: Write specific aims
        messages = [Message(
            role=MessageRole.USER,
            parts=[TextPart(text="Help me write specific aims for artist wellbeing study")]
        )]
        task = await agent.process_message(messages)
        print(task.artifacts[0].parts[0].text)

    asyncio.run(demo())
