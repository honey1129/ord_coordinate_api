from sqlalchemy.orm import Session


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
    return {'data': [dict(item._mapping) for item in db.execute(sql_str).all()]}

def get_coordinates_info_by_coordinate(db: Session, coordinate: str):
    sql_str = f'''
                SELECT
                  * 
                FROM
                    ordcoordinates 
                WHERE
                    coordinates = "{coordinate}" 
            '''
    return {'data': [dict(item._mapping) for item in db.execute(sql_str).all()]}
