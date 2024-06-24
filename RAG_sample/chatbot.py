import os
from dotenv import load_dotenv
import openai
from langchain_postgres.vectorstores import PGVector
from langchain_openai import OpenAIEmbeddings

load_dotenv()

# Initialize OpenAI and PostgreSQL client
api_key = os.environ.get("OPEN_AI_KEY")
openai.api_key = api_key
client = openai.Client(api_key=api_key)

db_url = os.environ.get("POSTGRES_CONNECTION_STRING")
embeddings = OpenAIEmbeddings(api_key=api_key)

vector_store = PGVector(
    embeddings=embeddings,
    collection_name="your_collection_name",
    connection=db_url,
    use_jsonb=True
)

def get_response_from_vector_store(prompt):
    # This function will use the vector store to find the most relevant response
    documents = vector_store.search(prompt)
    if documents:
        return documents[0].content  # Assuming the most relevant document's content is the response
    return "I'm not sure how to respond to that."

def get_completions(prompt):
    #documents = vector_store.search(prompt)
    #prompt = f"Here is the context: {documents[0].page_content} \n\n {prompt}"
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

def start_chatbot():
    print("Chatbot: Hello! How can I assist you today?")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ['exit', 'quit']:
            print("Chatbot: Goodbye!")
            break
        response = get_completions(user_input)
        print(f"Chatbot: {response}")

if __name__ == "__main__":
    start_chatbot()
