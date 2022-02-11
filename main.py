import uvicorn
from fastapi import FastAPI
import os
from typing import List
from fastapi_sqlalchemy import DBSessionMiddleware
from fastapi_sqlalchemy import db
from models import Customer as ModelCustomer
from schema import Customer as SchemaCustomer
from models import MeterType as ModelMeterType
from schema import MeterType as SchemaMeterType
from dotenv import load_dotenv
from fastapi.responses import HTMLResponse

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, "alembic/.env"))


app = FastAPI()

app.add_middleware(DBSessionMiddleware, db_url=os.environ["DATABASE_URL"])


@app.post("/customer/", response_model=SchemaCustomer)
async def create_customer(customer: SchemaCustomer):
    db_customer = ModelCustomer(
        id=customer.id, uuid=customer.uuid, name=customer.name, email=customer.email
    )
    db.session.add(db_customer)
    db.session.commit()
    return db_customer


@app.post("/meter/", response_model=SchemaMeterType)
async def create_meter(meter: SchemaMeterType):
    db_meter = ModelMeterType(
        id=meter.id, uuid=meter.uuid, name=meter.name, description=meter.description, customer_id=meter.customer_id)
    db.session.add(db_meter)
    db.session.commit()
    return db_meter


@app.post('/customer/detail/{id}', response_model=SchemaCustomer)
async def detail(id: int):
    detail_customer = db.session.get(ModelCustomer, id)
    return detail_customer


@app.post('/meter/detail/{id}', response_model=SchemaMeterType)
async def detail(id: int):
    detail_meter = db.session.get(ModelMeterType, id)
    return detail_meter


@app.delete('/customer/{id}', response_model=List[SchemaCustomer])
async def delete_customer(id: int):
    delete = db.session.get(ModelCustomer, id)
    db.session.delete(delete)
    db.session.commit()
    return {"Deleted"}
                

@app.delete('/meter/{id}', response_model=List[SchemaMeterType])
async def delete_meter(id: int):

    delete = db.session.get(ModelMeterType, id)
    db.session.delete(delete)
    db.session.commit()
    return {"Deleted"}


@app.put('/meter/{id}', response_model=SchemaMeterType)
async def put_meter(id: int, meter: SchemaMeterType):
    delete = db.session.get(ModelMeterType, id)
    hero_data = meter.dict(exclude_unset=True)
    for key, value in hero_data.items():
        setattr(delete, key, value)
    db.session.add(delete)
    db.session.commit()
    db.session.refresh(delete)
    return delete


@app.put('/customer/{id}', response_model=SchemaCustomer)
async def put_customer(id: int, customer: SchemaCustomer):
    delete = db.session.get(ModelCustomer, id)
    hero_data = customer.dict(exclude_unset=True)
    for key, value in hero_data.items():
        setattr(delete, key, value)
    db.session.add(delete)
    db.session.commit()
    db.session.refresh(delete)
    return delete


@app.post('/meter/type/{id}', response_model=List[SchemaMeterType])
async def search_meter(id: int):
    return db.session.query(ModelMeterType).filter(ModelMeterType.customer_id == id).all()
