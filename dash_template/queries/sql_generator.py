from langchain.chat_models import ChatOpenAI
from langchain.chains import Chain
from langchain.prompts import PromptTemplate

# Initialize the OpenAI API (replace 'your-openai-api-key' with your actual API key)
openai_api_key = 'your-openai-api-key'
openai_model = ChatOpenAI(openai_api_key)

# Define a prompt template for converting natural language to SQL
prompt_template = PromptTemplate(
    template="Convert the following natural language query to a SQL query: {nl_query}",
    input_variables=["nl_query"]
)

# Define a chain that takes a natural language query and returns a SQL query
sql_chain = Chain(model=openai_model, prompt_template=prompt_template)

def natural_language_to_sql(nl_query):
    """
    Convert a natural language query to a SQL query using LangChain.

    Args:
        nl_query (str): The natural language query.

    Returns:
        str: The generated SQL query.
    """
    result = sql_chain.run({"nl_query": nl_query})
    return result

class SQLQuery:
    def __init__(self, dataset, columns='*', limit=100):
        self.dataset = dataset
        self.columns = columns
        self.limit = limit

    def generate_query(self):
        """
        Generate the SQL query string.

        Returns:
            str: The SQL query string.
        """
        columns_str = ', '.join(self.columns) if isinstance(self.columns, list) else self.columns
        return f"SELECT {columns_str} FROM {self.dataset} LIMIT {self.limit}"
