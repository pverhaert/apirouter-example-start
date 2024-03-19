from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import config
import database
from models import models
from queries import festival_queries as queries

app = FastAPI(docs_url=config.documentation_url)

origins = config.cors_origins.split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/festivals")
def get_all_festivals():
    query = queries.festival_name_query
    festivals = database.execute_sql_query(query)
    if isinstance(festivals, Exception):
        return festivals, 500
    festivals_to_return = []
    for festival in festivals:
        festivals_to_return.append(festival[0])
    return({'festivals': festivals_to_return})

@app.get("/province")
def get_all_festivals_by_province(name: str):
    query = queries.festivals_by_province_query
    festivals = database.execute_sql_query(query, (
        name,
    ))
    if isinstance(festivals, Exception):
        return festivals, 500
    festivals_to_return = []
    for festival in festivals:
        festivals_to_return.append(festival[0])
    return({'festivals': festivals_to_return})

@app.get("/name_and_month")
def get_all_festivals_by_name_and_month(name: str, month: int):
    query = queries.festivals_by_name_and_month_query
    festivals = database.execute_sql_query(query, (
        '%{}%'.format(name),
        month,
        month,
    ))
    if isinstance(festivals, Exception):
        return festivals, 500
    festivals_to_return = []
    for festival in festivals:
        location = festival[1] + ' (' + festival[4] + ')'
        festival_dictionary = {"name": festival[0],
                               "startDate": festival[2],
                               "endDate": festival[3],
                               "location": location }
        festivals_to_return.append(festival_dictionary)
    return({'festivals': festivals_to_return})

@app.post("/festival")
def create_festival(festival: models.Festival):
    query = queries.insert_festival_query
    success = database.execute_sql_query(query, (
        festival.name,
        festival.location,
        festival.startDate,
        festival.endDate,
        festival.province,
        festival.comment,
    ))
    if success:
        return festival