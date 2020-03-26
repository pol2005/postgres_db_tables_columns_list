import os
import sys
import django
from sqlalchemy import create_engine
from sqlalchemy.schema import MetaData

# import django settings so we can work with models
BASE_PATH = ''
os.chdir(BASE_PATH)
sys.path.append(os.getcwd())
os.environ['DJANGO_SETTINGS_MODULE'] = 'artur.settings'
django.setup()
from crud.models import DatabaseList, TableList, ColumnList  # import django models

# database settings. Use a superuser username to be able to catch all databases from database server
USERNAME = ''  # superuser username
PASSWORD = ''  # superuser password
URL = ''  # for local databases, localhost or 127.0.0.1 will do the trick


def update_django_model(db_list):
    q_init = [i.name for i in DatabaseList.objects.all()]  # make a list from queryset
    #  The following for loop go threw each database of database server separately and if database exists,
    #  continues to the next database. In case that doesn't exist, it loops over its tables and over its
    #  tables' columns and saves it in django database
    for db in db_list:
        if db[0] in q_init:
            print('Database {} already exists'.format(db[0]))
            continue  # database already exists
        else:
            conn = database_conn(USERNAME, PASSWORD, URL, db[0]).connect()
            m = MetaData()  # get metadata
            m.reflect(bind=conn)
            b = DatabaseList(name=db[0], author=db[1])  # prepare django model before save
            b.save()  # save in database
            for table in m.tables.values():
                c = TableList(name=table, db=b)  # prepare django model before save
                c.save()  # save in database
                for column in table.c:
                    d = ColumnList(name=column.name, column_type=column.type, table=c)  # prepare django model before save
                    d.save()  # save in database
            print('Database {} successfully imported'.format(db[0]))
            conn.close()


#  this function handles database connection to the server. We should connect always to postgres database
#  to retrieve the information we want.
def database_conn(username, password, url, database):
    connection_string = 'postgresql://{0}:{1}@{2}:5432/{3}'.format(username, password, url, database)
    eng = create_engine(connection_string)
    return eng


# this function returns a list of databases in server
def fetch_all_dbs(conn):
    #  this query retrieves all databases and their authors
    q = conn.execute('SELECT pg_database.datname, pg_authid.rolname FROM pg_database INNER JOIN pg_authid ON pg_database.datdba=pg_authid.oid;')
    available_databases = q.fetchall()
    standard_db_list = ['postgres', 'template0', 'template1', 'rdsadmin']  # normally we don't need these system databases
    db_list = []
    for name in available_databases:
        if name[0] not in standard_db_list:  # exclude standard postgres databases
            db_list.append(name)
    return db_list


def main():
    conn = database_conn(USERNAME, PASSWORD, URL, 'postgres').connect()
    update_django_model(fetch_all_dbs(conn))
    conn.close()


#  just run "python3 import.py" to run the script
if __name__ == '__main__':
    main()

