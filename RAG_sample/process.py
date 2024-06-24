import fitz
import re
import os
import openai
from dotenv import load_dotenv
from openai import OpenAI
from langchain.docstore.document import Document
from langchain_openai import OpenAIEmbeddings
from langchain_postgres.vectorstores import PGVector

load_dotenv()

### initialize openai client and vector store###
api_key = os.environ.get("OPEN_AI_KEY")
client = openai.Client(api_key=api_key)

embeddings = OpenAIEmbeddings(api_key=api_key)

#### PDF Preprocessing Functions####

db_url = os.environ.get("POSTGRES_CONNECTION_STRING")

vector_store = PGVector(
    embeddings=embeddings,
    collection_name="limitless_test",
    connection=db_url,
    use_jsonb=True
)

#you can also add 

def extract_text(page):
    '''Extract text from a page and returns a list of strings'''
    text = page.get_text(sort=True)
    text = text.split('\n')
    text = [t.strip() for t in text if t.strip()]

    return text


def compare(a, b):
    '''Fuzzy matching of strings to compare headers/footers in neighboring pages'''

    count = 0
    a = re.sub('\d', '@', a)
    b = re.sub('\d', '@', b)
    for x, y in zip(a, b):
        if x == y:
            count += 1
    return count / max(len(a), len(b))


def remove_header(pages, header_candidates, WIN):
    '''Remove headers from content dictionary. Helper function for remove_header_footer() function.'''

    header_weights = [1.0, 0.75, 0.5, 0.5, 0.5]

    for i, candidate in enumerate(header_candidates):
        temp = header_candidates[max(
            i-WIN, 1): min(i+WIN, len(header_candidates))]
        maxlen = len(max(temp, key=len))
        for sublist in temp:
            sublist[:] = sublist + [''] * (maxlen - len(sublist))
        detected = []
        for j, cn in enumerate(candidate):
            score = 0
            try:
                cmp = list(list(zip(*temp))[j])
                for cm in cmp:
                    score += compare(cn, cm) * header_weights[j]
                score = score/len(cmp)
            except:
                score = header_weights[j]
            if score > 0.5:
                detected.append(cn)
        del temp

        for d in detected:
            while d in pages[i][:5]:
                pages[i].remove(d)

    return pages


def remove_footer(pages, footer_candidates, WIN):
    '''Remove footers from content dictionary. Helper function for remove_header_footer() function.'''

    footer_weights = [0.5, 0.5, 0.5, 0.75, 1.0]

    for i, candidate in enumerate(footer_candidates):
        temp = footer_candidates[max(
            i-WIN, 1): min(i+WIN, len(footer_candidates))]
        maxlen = len(max(temp, key=len))
        for sublist in temp:
            sublist[:] = [''] * (maxlen - len(sublist)) + sublist
        detected = []
        for j, cn in enumerate(candidate):
            score = 0
            try:
                cmp = list(list(zip(*temp))[j])
                for cm in cmp:
                    score += compare(cn, cm)
                score = score/len(cmp)
            except:
                score = footer_weights[j]
            if score > 0.5:
                detected.append(cn)
        del temp

        for d in detected:
            while d in pages[i][-5:]:
                pages[i] = pages[i][::-1]
                pages[i].remove(d)
                pages[i] = pages[i][::-1]

    return pages


def chunk_page(page):
    chunks = []
    current_chunk = []
    word_count = 0

    for word in page:
        current_chunk.append(word)
        word_count += 1

        if word_count == 100:
            chunks.append(' '.join(current_chunk))
            current_chunk = []
            word_count = 0

    if current_chunk:
        chunks.append(' '.join(current_chunk))

    return chunks

#### langchain Ingest Functions####


def extract_entities_and_context_using_openai(text):
    try:
        completion = client.chat.completions.create(
            model="gpt-4",
            messages=[{
                "role": "system",
                "content": "You are a tool that helps me extract entities from a text chunk passed to you. The format of your output should be a list of dictionaries, where each dictionary has two keys: 'entity' and 'context'. The value of 'entity' should be a string representing the entity, and the value of 'context' should be a string representing the context in which the entity appears. For example, [{'entity': 'Apple', 'context': 'I love apples.'}]."
            },
                {"role": "user", "content": text}],
            temperature=0,
            max_tokens=500
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Error: {e} occurred"

#### Main Preprocessing Function####


def process(file_path, user_tags=None):
    pages = fitz.open(file_path)
    pages = [extract_text(page) for page in pages]

    header_candidates = []
    footer_candidates = []

    for page in pages:
        header_candidates.append(page[:5])
        footer_candidates.append(page[-5:])

    WIN = 8

    pages = remove_header(pages, header_candidates, WIN)
    pages = remove_footer(pages, footer_candidates, WIN)

    chunks = [chunk_page(page) for page in pages]
    docs = []
    for chunk in chunks:
        chunk = ' '.join(chunk)
        entity_data = extract_entities_and_context_using_openai(chunk)
        doc = Document(
            page_content=chunk,
            metadata=dict(
                source=file_path,
                num_tokens=len(chunk),
                user_tags='None',  # comes from the user at a file level if you build a UI, otherwise you have to figure out some other user tag method. 
                entities=entity_data,  # will come from entity extraction function
            )
        )
        docs.append(doc)

    vector_store.add_documents(docs)


if __name__ == "__main__":
    file_path = 'add file path here'
    process(file_path)
