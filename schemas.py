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
    totalRecords: int
    data: List[CoordinatesInfoItem]

    class Config:
        schema_extra = {
            "example": {
                "massage": "Get Coordinates Datas Success!",
                "code": 200,
                "totalRecords": 2,
                "data": [
                    {
                        "Coordinates": "(0, 0)",
                        "Inscription_Id": "0784d8f7cb33919a622a82de9fa1972b735494da60d6f047a12e834a6935f935i0",
                        "genesis_height": 780641,
                        "sats": 448341,
                        "timestamp": "2023-03-13T14:57:51"
                    },
                    {
                        "Coordinates": "(0, 1)",
                        "Inscription_Id": "c917b958be751849b3073f59a13c26cee900dd7337516fc23838eff2205869dci0",
                        "genesis_height": 780641,
                        "sats": 448344,
                        "timestamp": "2023-03-13T14:57:51"
                    }
                ]
            }
        }


class CalculateTextPostItem(BaseModel):
    content: str
    type: str

    class Config:
        schema_extra = {
            "example": {
                "content": '{\n \"p\": \"brc-721\",\n \"op\": \"mint\",\n \"tick\":\"Bitcoin-Azuki\",\n \"id\": '
                           '\"8122165\",\n \"ipfs\":\"ipfs://QmZcH4YvBVVRJtdn4RdbaqgspFU8gH6P9vomDpBVpAL3u4\"\n}',
                "type": "common-text",
            }
        }


class CalculateTextPost(BaseModel):
    data: List[CalculateTextPostItem]

    class Config:
        schema_extra = {
            "example": {[{
                "content": '{\n \"p\": \"brc-721\",\n \"op\": \"mint\",\n \"tick\":\"Bitcoin-Azuki\",\n \"id\": '
                           '\"8122165\",\n \"ipfs\":\"ipfs://QmZcH4YvBVVRJtdn4RdbaqgspFU8gH6P9vomDpBVpAL3u4\"\n}',
                "type": "common-text",
            }]
            }
        }


class CalculateTextResponseItem(BaseModel):
    fname: str
    fsize: int

    class Config:
        schema_extra = {
            "example": {
                "fname": "6d06daac9e7e4e44ae4986beb613f36e.txt",
                "fsize": 149,
            }
        }


class CalculateTextResponse(BaseModel):
    code: str
    msg: str
    data: Union[List[CalculateTextResponseItem], None] = None

    class Config:
        schema_extra = {
            "example": {
                "code": 0,
                "msg": "ok",
                "data": [{
                    "fname": "6d06daac9e7e4e44ae4986beb613f36e.txt",
                    "fsize": 149,
                }]
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
            "example": {
                "orderId": "1667466888291033088",
                "fundAddress": "bc1plpf8y9a2r3wj7c250g40dt7sxgdu0trlxylgnwr93x85gtg90kkqn0s73h",
                "btcPrice": 0.004246,
            }
        }


class CreateOrderResponse(BaseModel):
    code: int
    msg: str
    data: Union[OrderResponseItem, None] = None

    class Config:
        schema_extra = {
            "example": {
                "code": 0,
                "msg": "ok",
                "data": {
                    "orderId": "1667466888291033088",
                    "fundAddress": "bc1plpf8y9a2r3wj7c250g40dt7sxgdu0trlxylgnwr93x85gtg90kkqn0s73h",
                    "btcPrice": 0.004246,
                }
            }
        }


class ValidCoordinatesItem(BaseModel):
    valid_coordinate: str


class ValidCoordinatesResponse(BaseModel):
    code: int
    msg: str
    data: Union[List[ValidCoordinatesItem], None] = None

    class Config:
        schema_extra = {
            "example": {
                "code": 0,
                "msg": "ok",
                "data": [
                    {
                        "valid_coordinate": "(0,2)"
                    }
                ]
            }
        }
