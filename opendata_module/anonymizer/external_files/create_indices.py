import psycopg2 as pg
import os
import sys
import traceback
import datetime

ROOT_DIR = os.path.abspath(os.path.dirname(__file__))

sys.path.append(os.path.join(ROOT_DIR, '..'))

from settings import postgres, anonymizer


def get_connection_string(
        host_address=None, port=None, database_name=None, user=None, password=None, **irrelevant_settings):
    string_parts = ["host={host} dbname={dbname}".format(
        **{'host': host_address, 'dbname': database_name})]

    if port:
        string_parts.append("port=" + str(port))

    if user:
        string_parts.append("user=" + user)

    if password:
        string_parts.append("password=" + password)

    return ' '.join(string_parts)

connection_string = get_connection_string(**postgres)

if anonymizer['field_translations_file'].startswith('/'):
    field_translations_file_path = anonymizer['field_translations_file']
else:
    field_translations_file_path = os.path.join(ROOT_DIR, '../cfg_lists', anonymizer['field_translations_file'])

with open(field_translations_file_path) as field_translations_file:
    fields = {line.strip().split(' -> ')[1].lower() for line in field_translations_file if line.strip()}
    fields.add('requestindate')

table_name = postgres['table_name']

for field_name in sorted(fields):
    try:
        with pg.connect(connection_string) as connection:
            cursor = connection.cursor()
            cursor.execute("CREATE INDEX logs_{field_name}_idx ON {table_name} ({field_name});".format(**{
                'field_name': field_name,
                'table_name': table_name
            }))
            message = [
                ("[{current_time}] ".format(**{'current_time': datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')}) +
                 "Created index logs_{field_name}_idx with the command: ".format(**{'field_name': field_name})),
                "  CREATE INDEX logs_{field_name}_idx ON {table_name} ({field_name});".format(**{
                    'field_name': field_name,
                    'table_name': table_name
                })
            ]
            print('\n'.join(message))

    except:
        print("[{current_time}] ".format(**{'current_time': datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')}) +
              "Command failed:\n  CREATE INDEX logs_{field_name}_idx ON {table_name} ({field_name});".format(**{
                  'field_name': field_name,
                  'table_name': table_name
              }))
        traceback.print_exc()
