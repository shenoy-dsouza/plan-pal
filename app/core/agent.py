from langchain.agents import AgentExecutor
from langchain.prompts import PromptTemplate
from langchain.agents.format_scratchpad import format_log_to_str
from app.core.parser import CustomOutputParser
from app.core.tools import get_tools
from app.config.llm import llm
from langchain.tools.render import render_text_description


def create_agent() -> AgentExecutor:
    tools = get_tools()
    template = """You are an advanced AI travel planning assistant.Your task is to create comprehensive travel plans that include:
        1. A brief summary of the overall trip plan
        2. Detailed day-by-day itineraries with activities
        3. Precise budget breakdowns for each day
        4. Personalized recommendations for accommodations and dining
        5. Practical travel tips

        ALWAYS FORMAT YOUR FINAL ANSWER USING THESE EXACT SECTION HEADERS:
        ### Plan
        [brief overview of the trip: highlight key destinations, travel style, major activities, and budget approach]

        ### Itinerary
        Provide a detailed day-by-day plan in natural language. Do not include JSON or structured data unless specifically asked.

        ### Budget
        Break down the budget in natural language. Avoid using JSON format unless absolutely needed.

        ### Recommendations
        [accommodation and dining suggestions: include 2–3 places to stay and eat, with price ranges and short descriptions]

        ### Tips
        [travel tips: money-saving ideas, local hacks, safety/weather advice, best time to visit, etc.]

        When planning:
        - Always consider the travel style and budget constraints
        - Provide realistic time allocations for activities
        - Include estimated costs for each major activity
        - Suggest money-saving tips where possible
        - Offer alternatives in case of weather or timing issues

        Tools available:
        {tools}

        Use the following format:

        Question: the input question you must answer
        Thought: you should always think about what to do
        Action: the action to take, should be one of [{tool_names}]
        Action Input: the input to the action as a JSON string
        Observation: the result of the action
        ... (this Thought/Action/Action Input/Observation can repeat N times)
        Thought: I now know the final answer
        Final Answer: the final answer to the original input question

        Begin!

        Question: {input}
        Thought: {agent_scratchpad}"""

    prompt = PromptTemplate.from_template(template)
    prompt = prompt.partial(
        tools=render_text_description(tools),
        tool_names=", ".join([t.name for t in tools]),
    )

    agent = (
        {
            "input": lambda x: x["input"],
            "agent_scratchpad": lambda x: format_log_to_str(
                x["intermediate_steps"]
            ),
        }
        | prompt
        | llm
        | CustomOutputParser()
    )

    return AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        handle_parsing_errors="Check your output and make sure it conforms to the required format!",
        max_iterations=5,
        early_stopping_method="generate",
    )
