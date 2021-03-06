import pandas as pd
import cx_Oracle

cx_Oracle.init_oracle_client(lib_dir=r'~/instantclient_19_8',
                             config_dir=r'~/instantclient_19_8/network/admin/')

protocol == 'tcps'

def get_oracle_connection(query, mode, data_list=None):
    '''returns datafarame for select query and 1 if record is inserted'''

    df = pd.DataFrame()
    insert_return = 0
    # we form dns string to work with tcps protocol
    #connect_string="username/password@host:port/SID"
    try:
        if protocol == 'tcps':
            tcps_details = connect_string.replace("/", " ").replace("@", " ").replace(":", " ").split(" ")
            dns = "(DESCRIPTION = (ADDRESS_LIST = (ADDRESS = (PROTOCOL = TCPS)(HOST = " + tcps_details[
                2] + ")(PORT = " + tcps_details[3] + ")))(CONNECT_DATA = (SERVICE_NAME = " + tcps_details[4] + ")))"
            connection = cx_Oracle.connect(tcps_details[0], tcps_details[1], dns)
        else:
            connection = cx_Oracle.connect(connect_string)
        if mode == "read":
            df = pd.read_sql(query, con=connection)
            connection.commit()
            return df
        elif mode == "many":
            cursor = connection.cursor()
            cursor.executemany(query, data_list)
            connection.commit()
        elif mode == "proc":
            cursor = connection.cursor()
            cursor.callproc(query)
        else:
            cursor = connection.cursor()
            cursor.execute(query)
            insert_return = cursor.rowcount
            connection.commit()
            return df
    except cx_Oracle.DatabaseError as e:

        logger.error("There is a problem with sql", e)
        sys.exit(1)
    finally:
        connection.close()

#running select query
get_oracle_connection("select * from table_name", "read")

#running insert query
get_oracle_connection("insert into table_name (column1,column2) values (value1, vlaue2)", "insert")

#running a procedure
get_oracle_connection("PROCEDURE_NAME, "proc")

#inserting all of data in a list od dictionaries, each dictionary having column1,column2 as keys.

list_query ="insert into table_name (column1,column2) select :column1 column1, :column2 column2 FROM DUAL"
get_oracle_connection(list_query, "many", data_list)

#running a delete query
get_oracle_connection("DELETE FROM table_name WHERE column1 ="someghing" , "execute")


