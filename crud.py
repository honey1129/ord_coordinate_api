from sqlalchemy.orm import Session

import models


def get_all_coordinates_info(db: Session, offset: int, limit: int):
    sql_str = f'''
        SELECT
            * 
        FROM
            ordcoordinates 
        ORDER BY
        TIMESTAMP DESC
        LIMIT {limit} OFFSET {offset}
    '''
    total_records_sql_str = f'''
        SELECT
          COUNT(DISTINCT sats)AS total_records
        FROM
            ordcoordinates 
        ORDER BY
        TIMESTAMP DESC
                '''
    total_records = [dict(item._mapping) for item in db.execute(total_records_sql_str).all()][0]['total_records']
    return {'data': [dict(item._mapping) for item in db.execute(sql_str).all()], 'total_records': total_records}


def get_all_coordinates_info_no_limit(db: Session):
    sql_str = f'''
        SELECT
            * 
        FROM
            ordcoordinates 
        ORDER BY
        TIMESTAMP DESC
    '''

    return {'data': [dict(item._mapping) for item in db.execute(sql_str).all()]}

def get_coordinates_info_by_sats(db: Session, sats: int):
    sql_str = f'''
            SELECT
              * 
            FROM
                ordcoordinates 
            WHERE
                sats = {sats} 
        '''
    total_records_sql_str = f'''
            SELECT
              COUNT(DISTINCT sats)AS total_records
            FROM
                ordcoordinates 
            WHERE
                sats = {sats} 
            '''
    total_records = [dict(item._mapping) for item in db.execute(total_records_sql_str).all()][0]['total_records']
    return {'data': [dict(item._mapping) for item in db.execute(sql_str).all()], 'total_records': total_records}


def get_coordinates_info_by_coordinate(db: Session, coordinate: str):
    sql_str = f'''
                SELECT
                  * 
                FROM
                    ordcoordinates 
                WHERE
                    coordinates = "{coordinate}" 
            '''

    total_records_sql_str = f'''
                    SELECT
                      COUNT(DISTINCT sats)AS total_records
                    FROM
                        ordcoordinates 
                    WHERE
                       coordinates = "{coordinate}" 
                '''
    total_records = [dict(item._mapping) for item in db.execute(total_records_sql_str).all()][0]['total_records']
    return {'data': [dict(item._mapping) for item in db.execute(sql_str).all()], 'total_records': total_records}


def create_order_history_data(db:Session, order_id:str,sender_address:str,fund_address:str,btc_price:float):
    sql_str = f'''
        INSERT INTO 
            order_history_data_detail (order_id,sender_address,fund_address,btc_price)
        VALUES
            ("{order_id}","{sender_address}","{fund_address}",{btc_price});
                    '''
    db.execute(sql_str)
    db.commit()
    return True
