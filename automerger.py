import pandas as pd
import datetime
from string import Template
import cx_Oracle
import os
import getpass
import sys

path = os.getcwd()


class DataMerge:
    #TODO: Split get_data and auto_merger functions for few smaller

    @staticmethod
    def get_data(user, password):
        """
        The func makes request to the database and gives the result to
        the automerger which transforms the data and put in right places
        :param user: user_id
        :param password: inputed_password
        :return: connection
        """
        conns = pd.read_csv("PATH.csv", index_col="nazwa")
        conns = conns.loc["DATABASE"]
        dsn_tnsDMKK = cx_Oracle.makedsn(conns["host"], conns["port"],
                                        service_name=conns["service_name"])  # service_name=
        connectionUNO = cx_Oracle.connect(user, password, dsn_tnsDMKK)
        sql_file = open("PATH", "r")
        sql_file_query = sql_file.read()
        data_uf = pd.read_sql(sql_file_query, connectionUNO)
        return data_uf

    @staticmethod
    def auto_merger(data_uf, address2):
        """
        The fuc concat the data and in the other hand delete some columns from table
        then saves to two locations
        :param data_uf: result of get_data
        :param address2: file from the HD
        """
        left = data_uf
        right = pd.read_csv(address2, delimiter='|')

        data_uf_zew = left[['COL1', 'COL2', 'COL3',
                            
                            ]]
        data_ex_zew = right[[
           'COL1', 'COL2', 'COL4',
        ]]

        data_uf_zew.to_csv("PATH.csv")
        data_uf_zew.to_excel("PATH.xlsx")
        data_ex_zew.to_excel("PATH.xlsx")

        now = datetime.date.today()
        pathm = "PATH.csv"
        pathk = "PATH$data.csv"

        the_templatek = Template(pathk)
        outputk = the_templatek.substitute(data=now)

        merged_left = pd.merge(left, right, how='outer', on=['COL1', 'COL2'])
        # podsumowanie na dysk M
        merged_left.to_csv(pathm, sep='|')
        # podsumowanie na dysk K
        merged_left.to_csv(outputk, sep='|')

        left.to_csv("PATH.csv", sep='|')
        right.to_csv("PATH.csv", sep='|')

        print('Done without any issues')
        input('Press enter to end: ')


def interface():
    """
    The func generates user interface
    """
    print("==================== MENU ====================")
    print()

    choice = int(input("""
        1: Start Refreshing mMoto report.
        2: Exit.

        Please enter Your choice:  """))
    if choice == 1:
        address = DataMerge.get_data(user, password)
        address2 = "PATH.csv"
        DataMerge.auto_merger(address, address2)
        interface()
    elif choice == 2:
        sys.exit()
    else:
        print("You must select from 1 to 2!")
        print("Try again")
        interface()


if __name__ == '__main__':
    user = "ui_" + getpass.getuser()
    print('Type Your oracle password')
    password = getpass.getpass()
    interface()
    print('Done without any issues')
    input('Press enter to end: ')
