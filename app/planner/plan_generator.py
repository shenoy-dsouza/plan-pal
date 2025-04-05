from typing import Optional, Dict
from app.core.agent import create_agent


class TravelPlanner:
    def __init__(self):
        self.agent = create_agent()

    def plan_trip(
        self,
        destination: str,
        budget: int,
        days: int,
        style: Optional[str] = "general",
    ) -> Dict:
        daily_budget = round(budget / days)

        input_query = f"""
        Create a {days}-day trip plan for {destination} with:
        - Total budget: ₹{budget}
        - Style: {style}
        - Daily budget: ₹{daily_budget}
        
        FORMAT YOUR RESPONSE WITH THESE EXACT SECTION HEADERS:
        ### Plan
        Give a short summary of the trip and destination.

        ### Itinerary
        List the daily plan in natural language. DO NOT include any JSON or code blocks.

        ### Budget
        Explain the budget breakdown clearly in sentences. Avoid JSON.

        ### Recommendations
        Suggest good places to stay and eat.

        ### Tips
        Add helpful travel advice.

        Use bullet points or paragraphs, NOT code or JSON blocks.
        """

        try:
            result = self.agent.invoke({"input": input_query})
            if isinstance(result, dict) and "output" in result:
                output_text = result["output"]
                sections = self.extract_sections(output_text)
                return {
                    "status": "success",
                    "plan": output_text,
                    "sections": sections,
                }
            return {
                "status": "success",
                "plan": str(result),
                "sections": self.extract_sections(str(result)),
            }

        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
                "solution": "Try simplifying your request or increasing the budget",
            }

    def extract_sections(self, text: str) -> Dict:
        sections = {
            "planner": "",
            "itinerary": "",
            "budget": "",
            "recommendations": "",
            "tips": "",
        }

        lines = text.replace("\r\n", "\n").split("\n")
        current_section = None

        for line in lines:
            if line.strip().startswith("### Plan"):
                current_section = "planner"
            if line.strip().startswith("### Itinerary"):
                current_section = "itinerary"
            elif line.strip().startswith("### Budget"):
                current_section = "budget"
            elif line.strip().startswith("### Recommendations"):
                current_section = "recommendations"
            elif line.strip().startswith("### Tips"):
                current_section = "tips"
            if current_section and not line.strip().startswith("###"):
                sections[current_section] += line + "\n"

        return {k: v.strip() for k, v in sections.items()}
