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
    data: List[CoordinatesInfoItem]
