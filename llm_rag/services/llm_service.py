from datetime import datetime, time
from .chroma_vector_db import query_text, embed_text
from .google_generative_ai import llm_gemini_2_5_flash

def prepare_prompt(docs, user_query):
    context = "\n\n\n".join(docs[0])
    today = datetime.today()
    PROMPT_TEMPLATE = f"""
        You are an Eventizer Assistant. You help users with their queries about the events in our application.
        Try to answer the question with the given context if you can connect the question and the below context try to do it.
        You are working in Indian date and time. Dates for the events will be provided in the context if the user asks upcoming or past queries try to
        answer the queries with the given time and match try to answer the question some how that's at least a bit helpful. 
        
        If the query is not completely about the events such as off topic to other things respond with You cannot assist with that answer.
        only response with you dont when the context is really too far and explain why you cant answer the question.
        Data about the query would be provided below. Help users query with the context below.
        Today's date: {today}
        context: {context}
        Answer the below question using the above context.
        question: {user_query}
        If the context is not enough say so.
    """
    return PROMPT_TEMPLATE

def get_llm_response(user_query):
    retrieved_docs = query_text(user_query)['documents']
    print(f"Documents retrieved: {retrieved_docs}")
    response = llm_gemini_2_5_flash(prepare_prompt(retrieved_docs, user_query))
    return response.candidates[0].content.parts[0].text

def create_embeddings(event):
    event_datetime = datetime.combine(event.e_date, time.min)

    text = f"""
    The name of the event is {event.e_title}.
    The event type/category of the event is {event.e_category}
    The event will happen on {event.e_date} from {event.e_start_time} to {event.e_end_time}
    the details of the event,  {event.e_description}
    Location/venues of the event : {event.e_venue}
    """

    embed_text(text, event.id, event_datetime)

