import openai
import time
import json
from flask import session
from employee_data import get_employee_data

class ThreadManager:
    def __init__(self):
        self.client = openai
        self.thread = None

    def create_thread(self):
        if 'thread_id' not in session:
            thread_obj = self.client.beta.threads.create()
            session['thread_id'] = thread_obj.id
            self.thread = thread_obj
        else:
            self.thread = self.client.beta.threads.retrieve(thread_id=session['thread_id'])

    def add_message_to_thread(self, role, content):
        if self.thread:
            self.client.beta.threads.messages.create(thread_id=self.thread.id, role=role, content=content)

    def run_assistant(self, assistant_id, instructions):
        if self.thread:
            run = self.client.beta.threads.runs.create_and_poll(
                thread_id=self.thread.id,
                assistant_id=assistant_id,
                )
            #run = self.client.beta.threads.runs.create(thread_id=self.thread.id, assistant_id=assistant_id, instructions=instructions)
            #return run

            if run.status == 'completed':
                messages = self.client.beta.threads.messages.list(
                    thread_id=self.thread.id
                )
                summary = []

                last_message = messages.data[0]
                print("last_message: ")
                print(last_message)
                response = last_message.content[0].text.value
                summary.append(response)

                return "\n".join(summary)
            else:
                print(run.status)

            # Define the list to store tool outputs
            tool_outputs = []
            
            # Loop through each tool in the required action section
            for tool in run.required_action.submit_tool_outputs.tool_calls:
                arguments = json.loads(tool.function.arguments)
                if tool.function.name == "get_employee_data":
                    output = get_employee_data(employeeId=arguments["employeeId"])
                    print(f"Fetched Employee Data: {output}")
                    tool_outputs.append({"tool_call_id": tool.id, "output": output})
                else:
                    raise ValueError(f"Unknown function: {tool.function.name}")

            print("tool outputs::::")
            print(tool_outputs)
            # Submit all tool outputs at once after collecting them in a list
            if tool_outputs:
                try:
                    run = self.client.beta.threads.runs.submit_tool_outputs_and_poll(
                        thread_id=self.thread.id,
                        run_id=run.id,
                        tool_outputs=tool_outputs
                    )
                    print("Tool outputs submitted successfully.")
                except Exception as e:
                    print("Failed to submit tool outputs:", e)
            else:
                print("No tool outputs to submit.")
            
            print("Before run.status == 'completed'")
            if run.status == 'completed':
                messages = self.client.beta.threads.messages.list(
                    thread_id=self.thread.id
                )
                summary = []

                last_message = messages.data[0]
                print("last_message: ")
                print(last_message)
                response = last_message.content[0].text.value
                summary.append(response)

                return "\n".join(summary)
            else:
                print(run.status)

    def wait_for_completion(self, run):
        if self.thread and run:
            while True:
                time.sleep(5)
                run_status = self.client.beta.threads.runs.retrieve(
                    thread_id=self.thread.id, run_id=run.id
                )
                print(f"RUN STATUS:: {run_status.model_dump_json(indent=4)}")

                if run_status.status == "completed":
                    self.process_message()
                    break
                elif run_status.status == "requires_action":
                    print("Function Calling ::::::")
                    self.call_required_functions(
                        required_actions=run_status.required_action.submit_tool_outputs.model_dump(),
                        run=run
                    )

    def call_required_functions(self, required_actions, run):
        if not run:
            return
        tool_outputs = []

        for action in required_actions["tool_calls"]:
            func_name = action["function"]["name"]
            arguments = json.loads(action["function"]["arguments"])

            if func_name == "get_employee_data":
                output = get_employee_data(employeeId=arguments["employeeId"])
                print(f"Fetched Employee Data: {output}")
                tool_outputs.append({"tool_call_id": action["id"], "output": output})
            else:
                raise ValueError(f"Unknown function: {func_name}")

        print("Submitting outputs back to the Assistant...")
        self.client.beta.threads.runs.submit_tool_outputs(
            thread_id=self.thread.id, run_id=run.id, tool_outputs=tool_outputs
        )

    # def process_message(self):
    #     messages = self.client.beta.threads.messages.list(thread_id=self.thread.id)
    #     summary = []

    #     last_message = messages.data[0]
    #     response = last_message.content[0].text.value
    #     summary.append(response)

    #     return "\n".join(summary)
