import json
from typing import Union
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Query, Depends, HTTPException, Request
import schemas
from sqlalchemy.orm import Session
from database import engine, Base, SessionLocal
import crud
import requests

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


@app.get("/ord-coordinate-api/coordinates-info", response_model=schemas.CoordinatesInfoResponse)
async def get_coordinates_info(sats: Union[int, None] = Query(default=None),
                               coordinate: Union[str, None] = Query(default=None),
                               db: Session = Depends(get_db),
                               page: Union[int, None] = Query(default=0),
                               limit: Union[int, None] = Query(default=100)):
    if sats:
        sat_data = crud.get_coordinates_info_by_sats(db=db, sats=sats)
    elif coordinate:
        sat_data = crud.get_coordinates_info_by_coordinate(db=db, coordinate=coordinate)
    else:
        sat_data = crud.get_all_coordinates_info(db=db, offset=page * limit, limit=limit)
    total_data_list = sat_data.get('data')
    if total_data_list is None:
        raise HTTPException(status_code=404, detail="Coordinates Data Not Found!")
    for i in total_data_list:
        a = i['Coordinates'][1:-1].split(',')
        i['Coordinates'] = str(tuple([int(x) for x in a]))
    return {
        "massage": "Get Coordinates Datas Success!",
        "code": 200,
        "totalRecords":sat_data.get('total_records'),
        "data": total_data_list,
    }


@app.post("/ord-coordinate-api/calculate_text", response_model=schemas.CalculateTextResponse)
async def calculate_text(request: Request, item: schemas.CalculateTextPost):
    post_data = {
        "content": item.content,
        "type": "common-text"
    }
    res = requests.post("https://api.idclub.io//inscribe/calculateText", data=json.dumps(post_data),
                        headers={'Content-Type': 'application/json'})
    if res.status_code == 200 and res:
        res_json = res.json()
        if res_json.get('code') == 0 and res_json.get("msg") == "ok":
            return {
                "code": 0,
                "msg": "ok",
                "data": {
                    "fname": res_json.get("data").get("fname"),
                    "fsize": res_json.get("data").get("fsize")
                }
            }
        else:
            return {
                "code": 500,
                "msg": "error",
                "data": None
            }
    else:
        return {
            "code": 500,
            "msg": "error",
            "data": None
        }


@app.post("/ord-coordinate-api/create-order", response_model=schemas.CreateOrderResponse)
async def create_order(request: Request, item: schemas.OrderPost, db: Session = Depends(get_db)):
    post_data = {
        "bc1": item.bc1,
        "feerate": item.feerate,
        "fnameList": item.fnameList,
        "sender": "bitcat",
        "type": "common-text",
        "payType": "bitcoin",
        "postage": 546,
        "mintFee": 5000
    }

    res = requests.post("https://api.idclub.io/inscribe/createSimple", data=json.dumps(post_data),
                        headers={'Content-Type': 'application/json'})
    if res.status_code == 200 and res:
        res_json = res.json()
        if res_json.get('code') == 0 and res_json.get("msg") == "ok":
            assert crud.create_order_history_data(db=db, order_id=res_json.get("data").get("orderId"),
                                                  sender_address=item.bc1,
                                                  fund_address=res_json.get("data").get("fundAddress"), btc_price=str(
                    res_json.get("data").get("inscribeCalculate").get("btcPrice")))
            return {
                "code": 0,
                "msg": "ok",
                "data": {
                    "orderId": res_json.get("data").get("orderId"),
                    "fundAddress": res_json.get("data").get("fundAddress"),
                    "btcPrice": res_json.get("data").get("inscribeCalculate").get("btcPrice")
                }
            }



        else:
            return {
                "code": 500,
                "msg": "error",
                "data": None
            }
    else:
        return {
            "code": 500,
            "msg": "error",
            "data": None
        }
