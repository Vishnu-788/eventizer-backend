from datetime import date, datetime, time, timedelta

def day_bounds(d: date):
    start = int(datetime.combine(d, time.min).timestamp())
    end = int(datetime.combine(d + timedelta(days=1), time.min).timestamp())
    return start, end

def get_date_filter(query: str):
    q = query.lower()

    today = date.today()
    tomorrow = today + timedelta(days=1)
    yesterday = today - timedelta(days=1)

    upcoming_words = ["upcoming", "future", "coming", "next"]
    past_words = ["past", "previous", "last", "before"]
    today_words = ["today", "tonight", "now"]
    tomorrow_words = ["tomorrow", "tmrw", "next day"]
    yesterday_words = ["yesterday"]

    # ---- exact days ----
    if any(w in q for w in today_words):
        s, e = day_bounds(today)
        return {"$and": [{"event_ts": {"$gte": s}}, {"event_ts": {"$lt": e}}]}

    if any(w in q for w in tomorrow_words):
        s, e = day_bounds(tomorrow)
        return {"$and": [{"event_ts": {"$gte": s}}, {"event_ts": {"$lt": e}}]}

    if any(w in q for w in yesterday_words):
        s, e = day_bounds(yesterday)
        return {"$and": [{"event_ts": {"$gte": s}}, {"event_ts": {"$lt": e}}]}

    # ---- relative ----
    today_start, _ = day_bounds(today)

    if any(w in q for w in past_words):
        return {"event_ts": {"$lt": today_start}}

    if any(w in q for w in upcoming_words):
        return {"event_ts": {"$gte": today_start}}

    # ---- week logic ----
    if "this week" in q:
        start = today - timedelta(days=today.weekday())
        end = start + timedelta(days=7)
        s, _ = day_bounds(start)
        e, _ = day_bounds(end)
        return {"$and": [{"event_ts": {"$gte": s}}, {"event_ts": {"$lt": e}}]}

    if "next week" in q:
        start = today - timedelta(days=today.weekday()) + timedelta(days=7)
        end = start + timedelta(days=7)
        s, _ = day_bounds(start)
        e, _ = day_bounds(end)
        return {"$and": [{"event_ts": {"$gte": s}}, {"event_ts": {"$lt": e}}]}

    if "weekend" in q:
        saturday = today + timedelta((5 - today.weekday()) % 7)
        sunday = saturday + timedelta(days=1)

        s1, e1 = day_bounds(saturday)
        s2, e2 = day_bounds(sunday)

        return {
            "$or": [
                {"$and": [{"event_ts": {"$gte": s1}}, {"event_ts": {"$lt": e1}}]},
                {"$and": [{"event_ts": {"$gte": s2}}, {"event_ts": {"$lt": e2}}]},
            ]
        }

    return None