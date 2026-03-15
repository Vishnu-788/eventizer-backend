from llm_rag.services.chroma_vector_db import embed_text
from celery import shared_task
from events.models import Event


@shared_task
def create_embeddings(event_id):
    event = Event.objects.get(id=event_id)
    text = f"""
    The name of the event is {event.e_title}.
    The event type/category of the event is {event.e_category}
    The event will happen on {event.e_date} from {event.e_start_time} to {event.e_end_time}
    the details of the event,  {event.e_description}
    Location/venues of the event : {event.e_venue}
    """

    embed_text(text, event.id, event.e_start_time)
