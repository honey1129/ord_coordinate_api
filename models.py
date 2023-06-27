from sqlalchemy import Column, DateTime, String, func, Boolean
from sqlalchemy.dialects.mysql import INTEGER, FLOAT, TINYINT, BIGINT,DOUBLE
from database import Base


class OrderHistoryDataDetail(Base):
    __tablename__ = 'order_history_data_detail'
    id = Column(INTEGER(unsigned=True), primary_key=True, index=True, autoincrement=True, unique=True, nullable=False,
                comment='id')
    order_id = Column(String(128), primary_key=True, index=True, unique=True, nullable=False,
                      comment='order-id')
    sender_address = Column(String(128), index=True, nullable=False, comment='sender地址'),
    fund_address = Column(String(128), index=True, nullable=False, comment='fund_address'),
    btc_price = Column(String(128), index=True, nullable=False, comment='花费的btc')
    created_at = Column(DateTime, server_default=func.now(), comment='创建时间')
    update_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment='更新时间')

