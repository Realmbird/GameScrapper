# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import re
from datetime import datetime
from itemadapter import ItemAdapter


class OpencriticPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        # Clean TopCritic_Average and Critics_Recommend fields

        if 'TopCritic_Average' in adapter:
            adapter['TopCritic_Average'] = int(adapter['TopCritic_Average'].strip())
        
        if 'Critics_Recommend' in adapter:
            adapter['Critics_Recommend'] = int(adapter['Critics_Recommend'].strip().rstrip('%'))

        # Format date field
        if 'date' in adapter:
            date_str = adapter['date'].strip().rstrip(' -')
            try:
                adapter['date'] = datetime.strptime(date_str, '%b %d, %Y').date()
            except ValueError:
                adapter['date'] = None  # Or keep the original string

        # Clean publisher field and remove special characters
        if 'publisher' in adapter:
            adapter['publisher'] = re.sub(r'[\\]', '', adapter['publisher'].strip())

        # Clean platform field and remove special characters
        if 'platform' in adapter:
            adapter['platform'] = [re.sub(r'[\\]', '', plat.strip()) for plat in adapter['platform']]



        return item
