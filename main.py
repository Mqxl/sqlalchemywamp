import uvicorn
import asyncpg
from fastapi import FastAPI
import os
from sqlalchemy.sql import table, column, select, update, insert, delete
from typing import List
from fastapi_sqlalchemy import DBSessionMiddleware
from fastapi_sqlalchemy import db
from models import Customer as ModelCustomer
from schema import Customer as SchemaCustomer
from models import MeterType as ModelMeterType
from schema import MeterType as SchemaMeterType
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, "alembic/.env"))


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(DBSessionMiddleware, db_url=os.environ["DATABASE_URL"])


@app.post("/customer/")
async def create_customer(customer: SchemaCustomer):
    db.session.execute(insert(ModelCustomer).values(id=customer.id, uuid=customer.uuid, name=customer.name,
                                                    email=customer.email))
    db.session.commit()
    return 'Success'


@app.post("/meter/")
async def create_meter(meter: SchemaMeterType):
    db.session.execute(insert(ModelMeterType).values(
        id=meter.id, uuid=meter.uuid, name=meter.name, description=meter.description, customer_id=meter.customer_id))
    db.session.commit()
    return 'Success'


@app.post('/customer/detail/{id}')
async def detail(id: int):
    s = select(ModelCustomer)
    s = s.where(ModelCustomer.id == id)
    result = db.session.execute(s)
    out = result.fetchall()
    return out


@app.post('/meter/detail/{id}')
async def detail(id: int):
    s = select(ModelMeterType)
    s = s.where(ModelMeterType.id == id)
    result = db.session.execute(s)
    out = result.fetchall()
    return out


@app.delete('/customer/{id}')
async def delete_customer(id: int):
    s = delete(ModelCustomer)
    s = s.where(ModelCustomer.id == id)
    db.session.execute(s)
    db.session.commit()
    return "Deleted"
                

@app.delete('/meter/{id}')
async def delete_meter(id: int):
    s = delete(ModelMeterType)
    s = s.where(ModelMeterType.id == id)
    db.session.execute(s)
    db.session.commit()
    return "Deleted"


@app.put('/meter/{id}')
async def put_meter(id: int, meter: SchemaMeterType):
    u = update(ModelMeterType)
    u = u.values(
        id=meter.id, uuid=meter.uuid, name=meter.name, description=meter.description, customer_id=meter.customer_id)
    u = u.where(ModelMeterType.id == id)
    db.session.execute(u)
    db.session.commit()
    return 'updated'


@app.put('/customer/{id}')
async def put_customer(id: int, customer: SchemaCustomer):
    u = update(ModelCustomer)
    u = u.values(
        id=customer.id, uuid=customer.uuid, name=customer.name,
        email=customer.email)
    u = u.where(ModelCustomer.id == id)
    db.session.execute(u)
    db.session.commit()
    return "updated"


@app.post('/meter/type/{id}')
async def search_meter(id: int):
    s = select(ModelMeterType)
    s = s.where(ModelMeterType.customer_id == id)
    result = db.session.execute(s)
    out = result.fetchall()
    return out
