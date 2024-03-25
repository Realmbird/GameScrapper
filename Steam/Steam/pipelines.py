# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

from datetime import datetime
from itemadapter import ItemAdapter


class SteamPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if "date" in adapter:
            date_str = adapter["date"].strip().replace('\r\n','')
            try:
                adapter['date'] = datetime.strptime(date_str, '%b %d, %Y').date()
            except ValueError:
                adapter['date'] = None  # Or keep the original string
        
        if adapter.get('price'):
            if adapter['price'].lower() != 'free':
                price_str = adapter['price'].replace('$', '').replace(',', '').strip()
                try:
                    adapter['price'] = float(price_str)
                except ValueError:
                    adapter['price'] = None
            else:
                adapter['price'] = 0 


        for field in ['total_positive', 'total_negative', 'total_reviews', 'review_score']:
            if field in adapter and isinstance(adapter[field], str):
                try:
                    adapter[field] = int(adapter[field])
                except ValueError:
                    adapter[field] = None
        

        return item
