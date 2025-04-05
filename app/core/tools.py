import json
from typing import List
from langchain.agents import Tool
from app.config.llm import llm


def generate_itinerary(input_json: str) -> str:
    try:
        input_dict = json.loads(input_json)
        prompt = f"""Create a detailed {input_dict['days']}-day
                itinerary for {input_dict['destination']} with:
                - Style: {input_dict['style']}
                - Daily budget: ₹{input_dict['daily_budget']}
                - Include time slots, activities, costs, and travel time
                - Format in markdown with clear sections"""
        return llm.invoke(prompt)
    except Exception as e:
        return f"Error generating itinerary: {str(e)}"


def analyze_budget(input_json: str) -> str:
    try:
        input_dict = json.loads(input_json)
        prompt = f"""Analyze ₹{input_dict['total_budget']} budget for
                {input_dict['days']} days in {input_dict['destination']}:
                - Break down by category
                (accommodation, food, activities, transport)
                - Show daily allocations
                - Include cost-saving tips
                - Format in markdown with tables"""
        return llm.invoke(prompt)
    except Exception as e:
        return f"Error analyzing budget: {str(e)}"


def recommend_places(input_json: str) -> str:
    try:
        input_dict = json.loads(input_json)

        prompt = f"""Recommend places in {input_dict['destination']} for
            {input_dict['style']} travelers:
            - Budget level: {input_dict['budget_level']}
            - Include 3 accommodations with prices
            - Include 3 restaurants with cuisine types
            - Format in markdown with bullet points"""
        return llm.invoke(prompt)
    except Exception as e:
        return f"Error recommending places: {str(e)}"


def get_tools() -> List[Tool]:
    return [
        Tool(
            name="Itinerary_Planner",
            func=generate_itinerary,
            description=(
                "Generates a detailed day-wise itinerary "
                "including activities and estimated costs. "
                "Input should be a JSON string with keys: destination, days,"
                "style, daily_budget"
            ),
        ),
        Tool(
            name="Budget_Analyzer",
            func=analyze_budget,
            description=(
                "Analyzes the budget and provides detailed cost breakdowns"
                "for each category. "
                "Input should be a JSON string with keys:"
                "total_budget, days,destination, style"
            ),
        ),
        Tool(
            name="Place_Recommender",
            func=recommend_places,
            description=(
                "Recommends places to stay and eat based on budget and style. "
                "Input should be a JSON string with keys:"
                "destination, style, budget_level"
            ),
        ),
    ]
