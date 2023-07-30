import json
import asyncio
from aiohttp import ClientSession
from typing import Union
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Query, Depends, HTTPException, Request
import schemas
from sqlalchemy.orm import Session

import utils
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




@app.get("/ord-coordinate-api")
async def root():
    '''
    root api
    :return:
    '''
    return {"message": "welcome to use ord-coordinate-api"}


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
        "totalRecords": sat_data.get('total_records'),
        "data": total_data_list,
    }


@app.post("/ord-coordinate-api/calculate-text", response_model=schemas.CalculateTextResponse)
async def calculate_text(request: Request, item: schemas.CalculateTextPost):
    res_data_list = []
    post_data = {"contentList": [i.content for i in item.data]}
    res = requests.post("https://api.idclub.io/inscribe/calculateBatch", data=json.dumps(post_data),headers={'Content-Type': 'application/json'})
    if res.status_code == 200 and res:
        res_json = res.json()
        if res_json.get('code') == 0 and res_json.get("msg") == "ok":
            res_data_list.append({
                # "coordinate": i.content,
                "fname": res_json.get("data").get("fname"),
                "fsize": res_json.get("data").get("fsize")
            })

    return {
        "code": 0,
        "msg": "ok",
        "data": res_data_list
    }


# else:
#     return {
#         "code": 500,
#         "msg": "error",
#         "data": None
#     }


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


@app.get("/ord-coordinate-api/valid-coordinates", response_model=schemas.ValidCoordinatesResponse)
async def get_valid_coordinates(request: Request,
                                coordinate_x_min: int,
                                coordinate_x_max: int,
                                coordinate_y_min: int,
                                coordinate_y_max: int,
                                db: Session = Depends(get_db)):
    all_coordinates_str = []
    for i in range(coordinate_x_min, coordinate_x_max + 1):
        for y in range(coordinate_y_min, coordinate_y_max + 1):
            coordinate = (i, y)
            coordinate_str = str(tuple(coordinate))
            all_coordinates_str.append(coordinate_str)
    all_db_coordinates_str = []
    all_coordinates_data_list = crud.get_all_coordinates_info_no_limit(db=db)
    for i in all_coordinates_data_list['data']:
        try:
            a = i['Coordinates'].strip()[1:-1].strip().split(',')
            i['Coordinates'] = str(tuple([int(x) for x in a]))
        except:
            pass
        else:
            all_db_coordinates_str.append(i['Coordinates'])
    all_none_coordinates_data_list = utils.array_diff(all_coordinates_str, all_db_coordinates_str)
    valid_coordinate_response_list = [{"valid_coordinate": x.replace(' ', '')} for x in all_none_coordinates_data_list]
    return {
        "code": 0,
        "msg": "ok",
        "data": valid_coordinate_response_list
    }
