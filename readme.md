# OpenAI API Employee Assistant - Flask Application

This project is a Flask-based web application that integrates OpenAI’s API to create a personal assistant for employees. The assistant can handle queries related to employee benefits, career growth, and other organizational tasks by interacting with an AI model. 

## Features

- Create and manage OpenAI assistant threads.
- Answer employee queries such as "What are my benefits?" using the assistant.
- Generate random employee data using the Faker library.
- Manage conversations with multiple users using Flask's session.
- Serve a simple HTML interface for user interaction.

## Table of Contents

1. [Requirements](#requirements)
2. [Installation](#installation)
3. [Environment Variables](#environment-variables)
4. [Usage](#usage)
5. [Project Structure](#project-structure)
6. [Endpoints](#endpoints)

## Requirements

To run this project, you need the following:

- Python 3.8 or higher
- OpenAI API key (you can get it from the [OpenAI API page](https://beta.openai.com/signup/))

## Installation

1. **Clone the repository**:

   ```bash
   git clone <your-repo-url>
   cd <project-directory>
   ```

2. **Set up a virtual environment**:

Create and activate a Python virtual environment:
```bash
python -m venv venv
```

On Windows:
```bash
venv\Scripts\activate

On macOS/Linux:
```bash
source venv/bin/activate
```

3. **Install dependencies**:
Use the requirements.txt file to install all required Python packages:
```bash
pip install -r requirements.txt
```

## Environment Variables
You need to create a .env file in the root directory of your project to store sensitive information like your OpenAI API key and Flask secret key.

Example .env file:
```bash
SECRET_KEY=your_flask_secret_key
OPENAI_API_KEY=your_openai_api_key
```

To generate a SECRET_KEY, you can run the following Python code:

```bash
import secrets
print(secrets.token_hex(16))
```

## Usage
1. Run the Flask app:

After setting up the environment and installing dependencies, you can run the app using the following command:
```bash
python app.py
```

2. Access the web interface:

Open your web browser and go to http://127.0.0.1:5000. You should see the interface where you can interact with the assistant.

3. Submit a query:

Enter your query (for example: "What are my benefits?") and click "Assist Me" to get a response from the AI assistant.


## Explanation of Key Files

app.py: This is the main file that sets up the Flask application, defines routes, and handles user queries.
assistant_manager.py: Manages the creation and execution of the OpenAI assistant.
thread_manager.py: Handles user sessions and conversation threads with the assistant.
employee_data.py: Uses the Faker library to generate random employee data for the assistant to respond with.
index.html: The front-end where users interact with the assistant by submitting queries.

## Endpoints

/
Method: GET
Description: Renders the main page where users can enter their queries.

/assist
Method: POST
Description: Handles the user query, passes it to the OpenAI assistant, and returns the response.