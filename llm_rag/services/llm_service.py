from datetime import datetime, time
from .chroma_vector_db import query_text, embed_text
from .google_generative_ai import llm_gemini_2_5_flash

def prepare_prompt(docs, user_query):
    context = "\n\n\n".join(docs[0])
    today = datetime.today()
    PROMPT_TEMPLATE = f"""
        You are an Eventizer Assistant. You help users with their queries about the events in our application.
        If the query is not completely about the events such as off topic to other things respond with You cannot assist with that answer.
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
    Event title: {event.e_title}
    Event Category: {event.e_category}
    Event date: {event.e_date}
    Event start time: {event.e_start_time}
    Event end time: {event.e_end_time}
    Event Description: {event.e_category} based event. {event.e_description}
    Event Venue: {event.e_venue}
    """

    embed_text(text, event.id, event_datetime)

