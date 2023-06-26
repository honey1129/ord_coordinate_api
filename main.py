import json
from typing import Union
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Query, Depends, HTTPException, Request
import schemas
from sqlalchemy.orm import Session
from database import engine, Base, SessionLocal
import crud

app = FastAPI(title="Ord Coordinate Api Docs",
              description="Ord Coordinate API 接口文档",
              docs_url="/ord-coordinate-api/docs",
              redoc_url="/ord-coordinate-api/redoc",
              openapi_url="/ord-coordinate-api/openapi.json")

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)


# 数据库依赖
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/ord-coordinate-api/coordinates-info", response_model=schemas.CoordinatesInfoResponse)
async def get_coordinates_info(sats: Union[int, None] = Query(default=None),
                               db: Session = Depends(get_db),
                               page: Union[int, None] = Query(default=0),
                               limit: Union[int, None] = Query(default=100)):
    if sats:
        sat_data = crud.get_coordinates_info_by_sats(db=db, sats=sats)
    else:
        sat_data = crud.get_all_coordinates_info(db=db, offset=page * limit, limit=limit)
    total_data_list = sat_data.get('data')
    if total_data_list is None:
        raise HTTPException(status_code=404, detail="Coordinates Data Not Found!")
    return {
        "massage": "Get Coordinates Datas Success!",
        "code": 200,
        "data": total_data_list,
    }
