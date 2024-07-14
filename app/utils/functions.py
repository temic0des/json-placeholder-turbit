from typing import List
from beanie import Document
import pymongo
from app.common.models.counter_model import Counter

async def initialize_counter(models: List[type[Document]]):
    for model in models:
        collection_name = model.get_collection_name()
        if collection_name == 'counters':
            continue
        max_id = await model.find().sort((model.id, pymongo.DESCENDING)).limit(1).first_or_none()
        if not max_id:
            return None
        collection_value = max_id.id
        counter = await Counter.find_one(Counter.collection_name == collection_name)
        if counter:
            counter.collection_value = collection_value
            await counter.save()
        else:
            new_counter = Counter(collection_name=collection_name, collection_value=collection_value)
            await Counter.insert_one(new_counter)

async def get_next_id(col_name: str) -> int:
    counter = await Counter.find_one(Counter.collection_name == col_name)
    if not counter:
        counter = Counter(collection_name=col_name, collection_value=0)

    counter.collection_value += 1
    await counter.save()
    return counter.collection_value