import openai

class AssistantManager:

    assistant_id = None

    def __init__(self, model: str = "gpt-4-turbo-preview"):
        self.client = openai
        self.model = model
        self.assistant = None

        # Retrieve existing assistant if ID is already set
        if AssistantManager.assistant_id:
            self.assistant = self.client.beta.assistants.retrieve(assistant_id=AssistantManager.assistant_id)
        else:
            self.create_assistant(
                name="Employees' Assistant",
                instructions="""You are a personal assistant to help organization employees with their queries.
                You should use the required functions to get employee's private and use company's doc to find relevant information to give personalized response. Keep the responses less than 20 characters.
                Don't make up any info on your own. Only rely on data you fetch using functions and files provided.""",
                tools=[
                    {
                        "type": "function",
                        "function": {
                            "name": "get_employee_data",
                            "description": "Return the employee's private data from the database",
                            "parameters": {
                                "type": "object",
                                "properties": {
                                    "employeeId": {
                                        "type": "string",
                                        "description": "Unique ID of the employee"
                                    }
                                },
                                "required": ["employeeId"]
                            }
                        }
                    },
                    {"type": "file_search"}
                ],

            )

    def create_assistant(self, name, instructions, tools):
        assistant_obj = self.client.beta.assistants.create(name=name, instructions=instructions, tools=tools,  model=self.model)
        AssistantManager.assistant_id = assistant_obj.id
        self.assistant = assistant_obj
