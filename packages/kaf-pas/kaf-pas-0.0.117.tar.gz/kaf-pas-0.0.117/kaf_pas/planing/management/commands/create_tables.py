import logging

from django.core.management import BaseCommand

from isc_common.common.mat_views import create_table, create_insert_update_delete_function_of_table

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    def handle(self, *args, **options):
        tablenames = ['planing_production_order']

        for tablename in tablenames:
            create_table(
                sql_str=f'''select * from {tablename}_view''',
                table_name=f'''{tablename}_tbl''',
                primary_key=['id'],
                indexes=[
                    'id',
                    'date',
                    'item_id',
                    'launch_id',
                    'num',
                    'isDeleted',
                    'opertype_id',
                    'parent_id',
                    'parent_item_id',
                    'props',
                    'status_id',
                ]
            )

            create_insert_update_delete_function_of_table(table_name=tablename)

        tablenames = ['planing_production_order_per_launch']

        for tablename in tablenames:
            create_table(
                sql_str=f'''select * from {tablename}_view''',
                table_name=f'''{tablename}_tbl''',
                primary_key=['id', 'launch_id'],
                indexes=[
                    'id',
                    'date',
                    'item_id',
                    'launch_id',
                    'num',
                    'opertype_id',
                    'parent_id',
                    'parent_item_id',
                    'props',
                    'status_id',
                ]
            )

            create_insert_update_delete_function_of_table(
                table_name=tablename,
                func_params=[('id', 'bigint'), ('launch_id', 'bigint')],
            )
