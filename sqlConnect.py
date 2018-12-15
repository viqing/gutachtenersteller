
import psycopg2
from sqlConfig import config
 
def connect(sqlFile):
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        params = config()
 
        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
 
        # create a cursor
        print('Creating cursor object...')
        cur = conn.cursor()
        
 # execute a statement
        # cur.execute(sqlFile)

        outputquery = 'copy ({0}) to stdout with csv header'.format(sqlFile)
        print(outputquery)

        with open('pyout.csv', 'w', encoding='utf-8') as f:
            cur.copy_expert(outputquery, f)

     # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')

 
if __name__ == '__main__':
    # Open and read the file as a single buffer
    with open(f'hagenholzstr96.sql', 'r') as fd:
        sqlFile = fd.read()
        connect(sqlFile)