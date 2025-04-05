import json
import re
from langchain.schema import AgentAction, AgentFinish
from langchain.agents import AgentOutputParser


class CustomOutputParser(AgentOutputParser):
    def parse(self, text: str) -> AgentAction | AgentFinish:
        if "Final Answer:" in text:
            return AgentFinish(
                return_values={
                    "output": text.split("Final Answer:")[-1].strip()
                },
                log=text,
            )

        action_match = re.search(
            r"Action:\s*(.+?)\s*Action Input:\s*(.+)", text, re.DOTALL
        )
        if action_match:
            action = action_match.group(1).strip()
            action_input = action_match.group(2).strip()

            if action_input.startswith("{") and action_input.endswith("}"):
                try:
                    json.loads(action_input)
                except json.JSONDecodeError:
                    action_input = action_input.replace("'", '"')
                    try:
                        json.loads(action_input)
                    except json.JSONDecodeError:
                        action_input = (
                            '{"error": "Could not parse action input"}'
                        )

            return AgentAction(tool=action, tool_input=action_input, log=text)

        return AgentFinish(return_values={"output": text}, log=text)
