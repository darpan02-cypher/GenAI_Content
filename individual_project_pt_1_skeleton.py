"""
Prompt Engineering Project
UNCC - Design and Development of Generative AI Applications

Name: <your name here>

"""

#BEFORE YOU BEGIN ============================================================

# You should have already completed the course-wide setup instructions.

# Before starting this assignment, make sure that:

# You have Python 3.13 installed.
# You have created and can activate your course virtual environment.
# Your virtual environment is activated: 
#   mac -> source venv/bin/activate
#   windows -> .\venv\Scripts\Activate.ps1
# You have a Groq account and API key.
# Your .env file contains your Groq API key: GROQ_API_KEY=your_api_key_here

# Do not submit your .env file or your API key.

#INSTALL THE REQUIRED PACKAGES ===============================================

# With your course virtual environment activated, install the two packages required for this assignment:

# Uncomment this line: 
#pip install groq python-dotenv 

# You do not need to create a new virtual environment for this assignment if you are using the virtual environment created for the course.

import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()  # Loads variables from .env

# Make sure you have your Groq API key saved in a .env file as GROQ_API_KEY 
GROQ_API_KEY = os.getenv('GROQ_API_KEY')

# ============================================================================
# Groq Client Wrapper
# ============================================================================

class GroqClient:
    """Wrapper class for Groq API interactions"""

    def __init__(self, api_key):
        """
        Initialize the Groq client

        Args:
            api_key (str): Groq API key
        """
        if not api_key:
            raise ValueError("API key is required")

        self.client = Groq(api_key=api_key)

    def call_llm(self, model_name, messages, reasoning_effort=None,
                 reasoning_format=None, include_reasoning=None):
        """
        Query the Groq API with a list of messages

        Args:
            model_name (str): The name of the model to use
            messages (list): List of message dictionaries with 'role' and 'content' keys
            reasoning_effort (str, optional): For reasoning models only (e.g. "low", "medium", "high")
            reasoning_format (str, optional): For reasoning models only (e.g. "parsed", "raw", "hidden")
            include_reasoning (bool, optional): For reasoning models only, whether to include
                the model's reasoning trace in the response

        Returns:
            str: The model's response or an error message
        """
        try:
            # TODO: Implement the Groq API call here
            # Hint: Use self.client.chat.completions.create()
            # - Set messages=messages
            # - Set model=model_name
            # - Set temperature value
            #   (Lower = more focused/deterministic, Higher = more creative/random)
            # - Extract and return the response content from completion.choices[0].message.content
            #
            # TODO (Reasoning models): At least one of your models (query models or evaluator)
            # must be a reasoning model, e.g. openai/gpt-oss-20b, openai/gpt-oss-120b,
            # openai/gpt-oss-safeguard-20b, or qwen/qwen3-32b.
            # Reasoning models support extra parameters documented here:
            # https://console.groq.com/docs/reasoning
            #   - reasoning_effort: controls how much the model "thinks" before answering
            #   - reasoning_format: controls how/whether reasoning is returned
            #   - include_reasoning: whether to include the reasoning trace at all
            # Only pass these kwargs to the API call when they are not None, since
            # non-reasoning models will error out if you send them unsupported params.
            # Example:
            #   kwargs = {"model": model_name, "messages": messages, "temperature": ...}
            #   if reasoning_effort is not None:
            #       kwargs["reasoning_effort"] = reasoning_effort
            #   if reasoning_format is not None:
            #       kwargs["reasoning_format"] = reasoning_format
            #   if include_reasoning is not None:
            #       kwargs["include_reasoning"] = include_reasoning
            #   completion = self.client.chat.completions.create(**kwargs)

            pass  # Remove this line when you implement the function

        except Exception as e:
            return f"Error querying the LLM: {e}"


# ============================================================================
# Chatbot class
# ============================================================================

class PythonHelpBot:
    """Command-line chatbot that compares LLM responses using different prompting techniques"""

    # TODO: Define the models to use for comparison.
    # You need 4 models that answer the user's question (MODEL_A - MODEL_D) plus
    # 1 evaluator model (EVALUATOR_MODEL). At least ONE of your five models must be
    # a reasoning model: openai/gpt-oss-20b, openai/gpt-oss-120b,
    # openai/gpt-oss-safeguard-20b, or qwen/qwen3-32b.
    # See available models here: https://console.groq.com/playground
    MODEL_A = ""  # TODO: Add model name here
    MODEL_B = ""  # TODO: Add model name here
    MODEL_C = ""  # TODO: Add model name here
    MODEL_D = ""  # TODO: Add model name here
    EVALUATOR_MODEL = ""  # TODO: Add evaluator model name here

    # TODO: If you want to try different reasoning settings for a reasoning model,
    # you can set defaults here (or None to omit them entirely). See:
    # https://console.groq.com/docs/reasoning
    REASONING_EFFORT = None      # e.g. "low", "medium", "high"
    REASONING_FORMAT = None      # e.g. "parsed", "raw", "hidden"
    INCLUDE_REASONING = None     # e.g. True / False

    # Prompting technique options
    # TODO: Add at least 3 different prompting techniques total (you can add more than
    # the 3 listed below, e.g. Role-Based, Self-Consistency, ReAct, etc.)
    PROMPT_TECHNIQUES = {
        "1": "Zero-Shot",
        "2": "Few-Shot",
        "3": "Chain-of-Thought"
        # plus any others you want to add
    }

    def __init__(self, groq_client):
        """
        Initialize the chatbot

        Args:
            groq_client (GroqClient): Instance of GroqClient for API interactions
        """
        self.groq_client = groq_client

        # System prompt (added at the start of every conversation)
        # TODO: Customize this system prompt for the Python Help Assistant
        self.system_prompt = """ """

        # TODO: Define your prompt templates here for the Python Help Assistant.
        # Each prompt should include a {user_query} placeholder that will be replaced
        # with the user's question at runtime. Make each technique meaningfully
        # different in how it instructs the model to answer (not just reworded).
        self.prompts = {
            "Zero-Shot": """TODO: Add your Zero-Shot prompt here
User query: {user_query}""",

            "Few-Shot": """TODO: Add your Few-Shot prompt here
User query: {user_query}""",

            "Chain-of-Thought": """TODO: Add your Chain-of-Thought prompt here
User query: {user_query}"""
        }

    def display_welcome(self):
        """Display welcome message"""
        print("\nWelcome to the Python Help Assistant!")
        print("\nThis chatbot will compare responses from four different models:")
        print(f"  Model A: {self.MODEL_A}")
        print(f"  Model B: {self.MODEL_B}")
        print(f"  Model C: {self.MODEL_C}")
        print(f"  Model D: {self.MODEL_D}")
        print(f"  Evaluator Model: {self.EVALUATOR_MODEL} (will assess which model's response is better)")

    def display_prompt_techniques(self):
        """Display available prompting techniques"""
        print("\nChoose a prompting technique:")
        for key, technique in self.PROMPT_TECHNIQUES.items():
            print(f"{key}. {technique}")
        print("4. Exit")

    def get_user_input(self, prompt):
        """
        Get user input

        Args:
            prompt (str): Prompt to display to user

        Returns:
            str: User's input
        """
        return input(prompt).strip()

    def select_prompt_technique(self):
        """
        Handle prompt technique selection

        Returns:
            str: Selected prompt technique name, or None if invalid/exit
        """
        self.display_prompt_techniques()
        choice = self.get_user_input("Enter your choice (1, 2, 3, or 4 to exit): ")

        if choice == '4':
            return 'exit'

        if choice in self.PROMPT_TECHNIQUES:
            return self.PROMPT_TECHNIQUES[choice]
        else:
            print("Invalid choice! Please select 1, 2, 3, or 4.")
            return None

    def get_user_query(self):
        """
        Get the user's query

        Returns:
            str: User's query
        """
        print("\n" + "="*60)
        print("Please enter your Python programming question.")
        # TODO: Add an example question relevant to Python
        # e.g. print("Example: 'How do I make a for loop?'")
        print("Example: ")
        print("="*60)
        user_query = self.get_user_input("\nYour query: ")

        if not user_query:
            user_query = "How do I print hello world?"

        return user_query

    def query_model(self, model_name, prompt_type, user_query):
        """
        Query a single model with the user's question

        Args:
            model_name (str): Name of the model to query
            prompt_type (str): Type of prompt technique to use
            user_query (str): User's query

        Returns:
            str: Model's response
        """
        # Format the technique-specific prompt with the user's query
        user_message = self.prompts[prompt_type].format(user_query=user_query).strip()

        # Create messages list with system prompt and user message
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": user_message}
        ]

        # TODO: If model_name is a reasoning model, pass the REASONING_EFFORT /
        # REASONING_FORMAT / INCLUDE_REASONING class attributes through to call_llm
        # so you can experiment with those settings. Otherwise call it with defaults.
        response = self.groq_client.call_llm(model_name, messages)
        return response

    def evaluate_responses(self, response_a, response_b, response_c, response_d):
        """
        Use evaluator model to compare four responses

        Args:
            response_a (str): Response from Model A
            response_b (str): Response from Model B
            response_c (str): Response from Model C
            response_d (str): Response from Model D

        Returns:
            str: Evaluation result
        """
        # TODO: Create an evaluation prompt that compares the four responses
        # Your prompt should:
        # 1. Explain that you're comparing four responses to a Python question
        # 2. List criteria to consider (correctness, clarity, best practices)
        # 3. Include all four responses (A, B, C, D)
        # 4. Ask for a determination of which is better and why
        # Model your output format after the example in the assignment instructions:
        #   - Which response is better: <A/B/C/D>
        #   - Brief explanation of why: ...
        #   - Key strengths of the winning response: ...

        evaluation_prompt = """add your evaluation prompt here
Include:
- Instructions to compare response A, B, C, and D
- Criteria to evaluate 
- Request for which response is better (A, B, C, or D)

Response A:
{response_a}

Response B:
{response_b}

Response C:
{response_c}

Response D:
{response_d}
""".format(response_a=response_a, response_b=response_b, response_c=response_c, response_d=response_d)

        messages = [
            {"role": "system", "content": "You are an expert evaluator comparing responses."},
            {"role": "user", "content": evaluation_prompt}
        ]

        return self.groq_client.call_llm(self.EVALUATOR_MODEL, messages)

    def run_one_round(self, prompt_type):
        """
        Run a single round: get a query, query all four models, and evaluate the responses.

        Args:
            prompt_type (str): Selected prompting technique name
        """
        # Get user's query
        user_query = self.get_user_query()

        # Query all models
        print("\nQuerying all models...\n")

        print("="*80)
        print(f"MODEL A ({self.MODEL_A}):")
        print("="*80)
        response_a = self.query_model(self.MODEL_A, prompt_type, user_query)
        print(response_a)

        print("\n" + "="*80)
        print(f"MODEL B ({self.MODEL_B}):")
        print("="*80)
        response_b = self.query_model(self.MODEL_B, prompt_type, user_query)
        print(response_b)

        print("\n" + "="*80)
        print(f"MODEL C ({self.MODEL_C}):")
        print("="*80)
        response_c = self.query_model(self.MODEL_C, prompt_type, user_query)
        print(response_c)

        print("\n" + "="*80)
        print(f"MODEL D ({self.MODEL_D}):")
        print("="*80)
        response_d = self.query_model(self.MODEL_D, prompt_type, user_query)
        print(response_d)

        # Evaluate responses
        print("\n" + "="*80)
        print(f"EVALUATION ({self.EVALUATOR_MODEL})")
        print("="*80)
        evaluation = self.evaluate_responses(response_a, response_b, response_c, response_d)
        print(evaluation)
        print("="*80)

    def run(self):
        """Main chatbot execution"""
        self.display_welcome()

        # Select prompting technique
        prompt_type = self.select_prompt_technique()

        if prompt_type == 'exit':
            print("\nGoodbye!\n")
            return

        if not prompt_type:
            print("Invalid selection. Exiting.")
            return

        # Run the first round of querying + evaluation
        self.run_one_round(prompt_type)

        # TODO: After showing the evaluation, give the user a menu (matching the
        # example conversation in the assignment instructions):
        #   1. Continue conversation  -> ask another question using the SAME prompt_type
        #   2. Start new conversation with different prompting technique
        #       -> call self.select_prompt_technique() again and run another round
        #   3. Exit -> print "Goodbye!" and stop
        # Hint: wrap this in a loop so the user can keep choosing options until they exit.

        print("\nGoodbye!\n")


# ============================================================================
# Main Entry Point
# ============================================================================

if __name__ == "__main__":
    # Initialize Groq client
    groq_client = GroqClient(GROQ_API_KEY)

    # Initialize and run chatbot
    chatbot = PythonHelpBot(groq_client)
    chatbot.run()