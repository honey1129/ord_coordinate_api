# -*- coding:utf-8 -*-
"""
Author: honey1129
Created time:2023/6/26 16:05
"""

from datetime import datetime
from typing import List, Union

from pydantic import BaseModel, Field


class CoordinatesInfoItem(BaseModel):
    Coordinates: str
    Inscription_Id: str
    genesis_height: int
    sats: int
    timestamp: datetime

    class Config:
        orm_mode = True


class CoordinatesInfoResponse(BaseModel):
    massage: str
    code: int
    totalRecords:int
    data: List[CoordinatesInfoItem]


class CalculateTextPost(BaseModel):
    content: str
    type: str

    class Config:
        schema_extra = {
            "content": '{\n \"p\": \"brc-721\",\n \"op\": \"mint\",\n \"tick\":\"Bitcoin-Azuki\",\n \"id\": '
                       '\"8122165\",\n \"ipfs\":\"ipfs://QmZcH4YvBVVRJtdn4RdbaqgspFU8gH6P9vomDpBVpAL3u4\"\n}',
            "type": "common-text",
        }


class CalculateTextResponseItem(BaseModel):
    fname: str
    fsize: int

    class Config:
        schema_extra = {
            "fname": "6d06daac9e7e4e44ae4986beb613f36e.txt",
            "fsize": 149,
        }


class CalculateTextResponse(BaseModel):
    code: str
    msg: str
    data: Union[CalculateTextResponseItem, None] = None

    class Config:
        schema_extra = {
            "code": 0,
            "msg": "ok",
            "data": {
                "fname": "6d06daac9e7e4e44ae4986beb613f36e.txt",
                "fsize": 149,
            }
        }


class OrderPost(BaseModel):
    bc1: str
    feerate: int
    fnameList: List[str]

    class Config:
        schema_extra = {
            "example": {
                "bc1": "bc1q7xdpudq8h8rl2mahv6qgj8rhlg2f7wewfp5fmg",
                "feerate": 15,
                "fnameList":
                    ["6d06daac9e7e4e44ae4986beb613f36e.txt"],
            }
        }


class OrderResponseItem(BaseModel):
    orderId: str
    fundAddress: str
    btcPrice: float

    class Config:
        schema_extra = {
            "orderId": "1667466888291033088",
            "fundAddress": "bc1plpf8y9a2r3wj7c250g40dt7sxgdu0trlxylgnwr93x85gtg90kkqn0s73h",
            "btcPrice": 0.004246,
        }


class CreateOrderResponse(BaseModel):
    code: int
    msg: str
    data: Union[OrderResponseItem, None] = None

    class Config:
        schema_extra = {
            "code": 0,
            "msg": "ok",
            "data": {
                "orderId": "1667466888291033088",
                "fundAddress": "bc1plpf8y9a2r3wj7c250g40dt7sxgdu0trlxylgnwr93x85gtg90kkqn0s73h",
                "btcPrice": 0.004246,
            }
        }
