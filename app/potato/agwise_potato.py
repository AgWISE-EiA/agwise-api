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

    def filter_data(self, filter_data, paginate):
        """
        Fetch the fertilizer recommendation data
        :param filter_data: fields to be filtered out
        :param paginate: enable or disable pagination
        :return:
        """
        session = self.session()
        query = session.query(FrPotatoApi)
        self.logging.debug(f"Processing requests --> {filter_data}")

        province = filter_data.get('Province')
        season = filter_data.get('Season')
        district = filter_data.get('District')
        aez = filter_data.get('AEZ')

        if province:
            query = query.filter(FrPotatoApi.Province.ilike(f"%{province}%"))
        if season:
            query = query.filter(FrPotatoApi.Season.ilike(f"%{season}%"))
        if district:
            query = query.filter(FrPotatoApi.District.ilike(f"%{district}%"))
        if aez:
            query = query.filter(FrPotatoApi.AEZ.ilike(f"%{aez}%"))

        # Parse the limit and offset parameters from the request
        limit = int(filter_data.get('limit', 100))  # Default limit is 100 records, change as needed
        page = int(filter_data.get('page', 1))  # Default page is 1, change as needed

        # Calculate the offset
        offset = (page - 1) * limit

        if paginate:
            total_records = query.count()
            total_pages = (total_records // limit + (1 if total_records % limit != 0 else 0))
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
                # 'lat': item.latitude,
                # 'lon': item.longitude,
                'coordinates': {
                    'lat': item.latitude,
                    'lon': item.longitude,
                },
                # 'coordinates': f'{item.latitude},{item.longitude}',
                'urea': float(item.Urea),
                'dap': float(item.DAP),
                'npk': float(item.NPK),
                'expectedYield': float(item.expectedYieldReponse),
                'fertilizerCost': float(item.totalFertilizerCost),
                'netRevenue': float(item.netRevenue)
            })
            filter_data = {
                'data': result,
            }
            if paginate:
                filter_data['pagination'] = {
                    'page': page,
                    'per_page': limit,
                    'total_records': total_records,
                    'total_pages': total_pages,
                    'last_page': total_pages
                }

        return filter_data
