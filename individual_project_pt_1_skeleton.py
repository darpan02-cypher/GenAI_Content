"""
Prompt Engineering Project
UNCC - Design and Development of Generative AI Applications

Name: Himanshi Shrivas

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
            #----------------------------start original TODO----------------------------
            
            # # We build the kwargs dict conditionally because reasoning_effort /
            # reasoning_format / include_reasoning are ONLY accepted by reasoning
            # models (gpt-oss-*, qwen3-32b). Sending them to a plain chat model
            # (like llama-3.x) raises an API error, so we only add the key if the
            # caller actually passed a value for it.
            
            kwargs = {
                "model": model_name,
                "messages": messages,
                "temperature": 0.7,  # balanced: not fully deterministic, not too random
            }
 
            if reasoning_effort is not None:
                kwargs["reasoning_effort"] = reasoning_effort
            if reasoning_format is not None:
                kwargs["reasoning_format"] = reasoning_format
            if include_reasoning is not None:
                kwargs["include_reasoning"] = include_reasoning
 
            completion = self.client.chat.completions.create(**kwargs)
 
            # The actual text answer lives at choices[0].message.content
            return completion.choices[0].message.content
            # ----- END ORIGINAL TODO -----
 
            

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
    # NOTE: llama-3.3-70b-versatile, llama-3.1-8b-instant, and qwen/qwen3-32b have
    # been decommissioned from Groq's catalog (confirmed via GET /openai/v1/models).
    # Swapped in currently available models below.
    MODEL_A = "openai/gpt-oss-120b"  # Reasoning-focused flagship (120B) open-weight model
    MODEL_B = "groq/compound-mini"  # Lightweight/fast model for contrast against the 120B flagship
    MODEL_C = "openai/gpt-oss-20b"  # Required reasoning-focused open-weight model
    MODEL_D = "qwen/qwen3.6-27b"  # Alibaba Qwen3 reasoning model for architectural variety
    EVALUATOR_MODEL = "openai/gpt-oss-120b"  # Acts as the LLM-as-judge to evaluate and rank outputs

    # TODO: If you want to try different reasoning settings for a reasoning model,
    # you can set defaults here (or None to omit them entirely). See:
    # https://console.groq.com/docs/reasoning
    #
    # NOTE: reasoning_format and include_reasoning are mutually exclusive on Groq's
    # API ("cannot specify both `include_reasoning` and `reasoning_format`") -- only
    # set one of the two. We use include_reasoning and leave reasoning_format unset
    # (the gpt-oss models on this account also reject reasoning_format="raw").
    REASONING_FORMAT = None      # e.g. "parsed", "raw", "hidden"
    INCLUDE_REASONING = True     # must stay None while REASONING_FORMAT is set

    # NOTE: valid reasoning_effort values differ by model family -- gpt-oss models
    # require "low"/"medium"/"high" while qwen3.6 requires "none"/"default". Rather
    # than one shared value, each reasoning model gets its own supported effort (or
    # None to omit the kwarg entirely).
    REASONING_EFFORT_BY_MODEL = {
        "openai/gpt-oss-20b": "medium",
        "openai/gpt-oss-120b": "medium",
        "openai/gpt-oss-safeguard-20b": "medium",
        "qwen/qwen3.6-27b": "default",
    }

        # Set of model names that support the reasoning_* kwargs. Used by query_model()
    # to decide whether to forward REASONING_FORMAT/INCLUDE_REASONING/reasoning_effort.
    REASONING_MODELS = {
        "openai/gpt-oss-20b",
        "openai/gpt-oss-120b",
        "openai/gpt-oss-safeguard-20b",
        "qwen/qwen3.6-27b",
    }

    # Prompting technique options
    # TODO: Add at least 3 different prompting techniques total (you can add more than
    # the 3 listed below, e.g. Role-Based, Self-Consistency, ReAct, etc.)
    PROMPT_TECHNIQUES = {
        "1": "Zero-Shot",
        "2": "Few-Shot",
        "3": "Chain-of-Thought",
        "4": "Role-Based"  #  additional technique
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
        self.system_prompt = (
            "You are a helpful Python programming assistant for students learning "
            "to code. Answer clearly and correctly, and keep explanations focused "
            "on the question asked."
        )

        # TODO: Define your prompt templates here for the Python Help Assistant.
        # Each prompt should include a {user_query} placeholder that will be replaced
        # with the user's question at runtime. Make each technique meaningfully
        # different in how it instructs the model to answer (not just reworded).
        self.prompts = {
            "Zero-Shot": """Answer the following Python programming question directly and concisely.
User query: {user_query}""",

            "Few-Shot": """You are answering Python programming questions. Follow the style of these examples:
 
Example 1:
Q: How do I reverse a list in Python?
A: Use slicing: `my_list[::-1]` returns a reversed copy without modifying the original.
```python
my_list = [1, 2, 3]
reversed_list = my_list[::-1]
```
 
Example 2:
Q: How do I check if a key exists in a dictionary?
A: Use the `in` keyword, which checks the dictionary's keys.
```python
my_dict = {{"a": 1}}
if "a" in my_dict:
    print("key exists")
```
 
Now answer this question in the same style (short explanation + code block):
User query: {user_query}""",

            "Chain-of-Thought": """Think through this Python question step by step before answering.
First, break down what the question is really asking.
Then reason through the solution logic step by step.
Finally, give the complete answer with a code example.
User query: {user_query}""",
            # Role-Based (extra technique): assigning the model a specific persona
        
            "Role-Based": """You are a senior Python developer mentoring a junior engineer during a code review.
Explain the answer the way you would to a mentee: clear reasoning, common pitfalls to avoid,
and a clean code example.
 
User query: {user_query}""",
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
        print(f"{self._exit_choice()}. Exit")

    def _exit_choice(self):
        """The menu number for 'Exit', placed right after the last technique."""
        return str(len(self.PROMPT_TECHNIQUES) + 1)

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
        exit_choice = self._exit_choice()
        valid_choices = ", ".join(self.PROMPT_TECHNIQUES.keys())
        choice = self.get_user_input(
            f"Enter your choice ({valid_choices}, or {exit_choice} to exit): "
        )

        if choice == exit_choice:
            return 'exit'

        if choice in self.PROMPT_TECHNIQUES:
            return self.PROMPT_TECHNIQUES[choice]
        else:
            print(f"Invalid choice! Please select {valid_choices}, or {exit_choice}.")
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
        
        print("Example: 'How do I read a CSV file into a list of dictionaries?'")
        # e.g. print("Example: 'How do I make a for loop?'")
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
        if model_name in self.REASONING_MODELS:
            response = self.groq_client.call_llm(
                model_name,
                messages,
                reasoning_effort=self.REASONING_EFFORT_BY_MODEL.get(model_name),
                reasoning_format=self.REASONING_FORMAT,
                include_reasoning=self.INCLUDE_REASONING
            )
        else:
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
        

        evaluation_prompt = """Compare the following four responses (A, B, C, D) to the same Python
programming question. Evaluate them using these criteria:
1. Correctness - is the code/explanation technically accurate?
2. Clarity - is the explanation easy to follow?
3. Best practices - does it follow good/idiomatic Python style?
 
Response A:
{response_a}
 
Response B:
{response_b}
 
Response C:
{response_c}
 
Response D:
{response_d}
 
Provide your evaluation in exactly this format:
- Which response is better: <A/B/C/D>
- Brief explanation of why: <your reasoning>
- Key strengths of the winning response: <bullet points>
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
        while True:
            print("\nWhat would you like to do next?")
            print("1. Continue conversation (ask another question, same technique)")
            print("2. Start new conversation with a different prompting technique")
            print("3. Exit")
            choice = self.get_user_input("Enter your choice (1, 2, or 3): ")
 
            if choice == "1":
                self.run_one_round(prompt_type)
            elif choice == "2":
                new_technique = self.select_prompt_technique()
                if new_technique == 'exit':
                    print("\nGoodbye!\n")
                    return
                if not new_technique:
                    continue  # invalid selection was already printed; ask again
                prompt_type = new_technique
                self.run_one_round(prompt_type)
            elif choice == "3":
                print("\nGoodbye!\n")
                return
            else:
                print("Invalid choice! Please select 1, 2, or 3.")
       


# ============================================================================
# Main Entry Point
# ============================================================================

if __name__ == "__main__":
    # Initialize Groq client
    groq_client = GroqClient(GROQ_API_KEY)

    # Initialize and run chatbot
    chatbot = PythonHelpBot(groq_client)
    chatbot.run()