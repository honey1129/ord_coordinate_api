from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import cfg
import pymysql

pymysql.install_as_MySQLdb()

engine = create_engine(cfg.get('db_eth_detail', 'uri'), encoding='utf-8', echo=True,)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, expire_on_commit=True)

Base = declarative_base(bind=engine, name='Base')
