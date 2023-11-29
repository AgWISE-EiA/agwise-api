from typing import Type

from sqlalchemy.orm import sessionmaker

from app.my_logger import MyLogger
from orm.database_conn import MyDb
from orm.models import FrPotatoApi


class AgWisePotato:
    def __init__(self):
        self.db_engine = MyDb()
        self.logging = MyLogger()
        self.session = sessionmaker(bind=self.db_engine)

    def filter_data(self, data):
        session = self.session()
        query = session.query(FrPotatoApi)
        self.logging.debug(f"Processing requests --> {data}")

        province = data.get('Province')
        season = data.get('Season')
        district = data.get('District')
        aez = data.get('AEZ')

        if province:
            query = query.filter(FrPotatoApi.Province.ilike(f"%{province}%"))
        if season:
            query = query.filter(FrPotatoApi.Season.ilike(f"%{season}%"))
        if district:
            query = query.filter(FrPotatoApi.District.ilike(f"%{district}%"))
        if aez:
            query = query.filter(FrPotatoApi.AEZ.ilike(f"%{aez}%"))

        # Parse the limit and offset parameters from the request
        limit = int(data.get('limit', 100))  # Default limit is 100 records, change as needed
        page = int(data.get('page', 1))  # Default page is 1, change as needed

        # Calculate the offset
        offset = (page - 1) * limit

        total_records = query.count()
        query = query.limit(limit).offset(offset)
        results = query.all()
        session.close()

        result = []
        item: Type[FrPotatoApi]
        for item in results:
            result.append({
                'id': item.id,
                'province': item.Province,
                'district': item.District,
                'aez': item.AEZ,
                'season': item.Season,
                'currentYield': item.refYieldClass,
                'lat': item.latitude,
                'lon': item.longitude,
                # 'coordinates': f'{item.latitude},{item.longitude}',
                'urea': float(item.Urea),
                'dap': float(item.DAP),
                'npk': float(item.NPK),
                'expectedYield': float(item.expectedYieldReponse),
                'fertilizerCost': float(item.totalFertilizerCost),
                'netRevenue': float(item.netRevenue)
            })
        total_pages = (total_records // limit + (1 if total_records % limit != 0 else 0))
        data = {
            'data': result,
            'pagination': {
                'page': page,
                'per_page': limit,
                'total_records': total_records,
                'total_pages': total_pages,
                'last_page': total_pages
            }
        }
        return data
