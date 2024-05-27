# Mark W Kiehl
# Mechatronic Solutions LLC
# V0.0.0

# Demonstrates the following with MySQL via Python:
#   Connect to MySQL as root user using mysql.connector
#   Get the current MySQL version
#   Get the MySQL users
#   Delete a MySQL user
#   Create a MySQL user
#   Create a database
#   Grant permissions to a MySQL user for a database
#   Get the current MySQL user
#   Create a new table for a datbase
#   Show all of the tables
#   Show all of the tables and the engine information for a database
#   Show detailed information about a table status
#   Show a table structure
#   Insert data into a table
#   Query a table
#   Repair a table
#   Delete a table, database, and user. 

# Git / GitHub
# Install Git
# Click on VSCode Source Control
# Click 'Initialize Repository"

def mysql_conn_as_root():
    import mysql.connector
    #from mysql.connector import errorcode
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="seas4summer"
        #"host": "127.0.0.1",
        #database='mydb01',
        #"raise_on_warnings": True
    )
    if not conn.is_connected(): raise Exception("Not connected to MySql")
    cur = conn.cursor()
    return conn, cur


def mysql_conn_as_user():
    import mysql.connector
    #from mysql.connector import errorcode
    conn = mysql.connector.connect(
        host="localhost",
        user="markwkiehl",
        password="seas4summer"
        #"host": "127.0.0.1",
        #database='mydb01',
        #"raise_on_warnings": True
    )
    if not conn.is_connected(): raise Exception("Not connected to MySql")
    cur = conn.cursor()
    return conn, cur


def mysql_user_exists(username=""):
    import mysql.connector
    found = False
    sql = """SELECT user FROM mysql.user;"""
    conn, cur = mysql_conn_as_root()
    try:
        cur.execute(sql)
        rows = cur.fetchall()
        if rows:
            #print("\n",sql)
            for row in rows:
                #print(row)
                if row[0] == username: 
                    found = True
                    break
        else:
            print("No result from query ", sql)
    except (mysql.connector.Error, mysql.connector.Warning) as e:
        print("MySQL error ", e)
    finally:
         cur.close()
         conn.close()
    return found


def main():
    # python3 -m pip install mysql-connector-python
    # pip install mysql-connector-python
    # pip install mysql-connector-python --upgrade
    import mysql.connector
    #from mysql.connector import errorcode


    conn, cur = mysql_conn_as_root()
    sql = """SELECT @@version;"""
    try:
        cur.execute(sql)
        row = cur.fetchone()
        if row:
            print("\nMySQL version:", row[0])
            #MySQL version: 8.0.36-2ubuntu3
        else:
            print("No result from query ", sql)
    except (mysql.connector.Error, mysql.connector.Warning) as e:
        print("MySQL error ", e)
    finally:
         cur.close()
         conn.close()

    # USER

    sql = """SELECT user FROM mysql.user;"""
    conn, cur = mysql_conn_as_root()
    try:
        cur.execute(sql)
        rows = cur.fetchall()
        if rows:
            print("\n" + sql)
            for row in rows:
                print(row)
        else:
            print("No result from query ", sql)
    except (mysql.connector.Error, mysql.connector.Warning) as e:
        print("MySQL error ", e)
    finally:
         cur.close()
         conn.close()

    sql = """DROP USER IF EXISTS markwkiehl@localhost;"""
    print("\n" + sql)
    conn, cur = mysql_conn_as_root()
    try:
        cur.execute(sql)
        # No result returned
    except (mysql.connector.Error, mysql.connector.Warning) as e:
        print("MySQL error ", e)
    finally:
         cur.close()
         conn.close()

    print("\nMySQL user 'markwkiehl' exists: ", mysql_user_exists('markwkiehl'))

    # CREATE USER [IF NOT EXISTS] '{username}'@'{hostname}' IDENTIFIED BY '{passwordString}';
    #sql = """CREATE USER IF NOT EXISTS 'markwkiehl'@'localhost' IDENTIFIED BY 'seas4summer';"""
    sql = """CREATE USER IF NOT EXISTS markwkiehl@localhost IDENTIFIED BY 'seas4summer';"""
    print("\n" + sql)
    conn, cur = mysql_conn_as_root()
    try:
        cur.execute(sql)
        # No result returned
    except (mysql.connector.Error, mysql.connector.Warning) as e:
        print("MySQL error ", e)
    finally:
         cur.close()
         conn.close()

    print("\nMySQL user 'markwkiehl' exists: ", mysql_user_exists('markwkiehl'))


    # DATABASE

    conn, cur = mysql_conn_as_root()
    # NOTE:  Only root can create a database
    sql = """CREATE DATABASE IF NOT EXISTS mydbtst;"""
    print("\n" + sql)
    try:
        cur.execute(sql)
        # No result returned
    except (mysql.connector.Error, mysql.connector.Warning) as e:
        print("MySQL error ", e)
    finally:
         cur.close()
         conn.close()

    sql = """SHOW DATABASES;"""
    sql = """SELECT schema_name FROM information_schema.schemata;"""
    # NOTE:  schemas returned varies by user (permissions).
    conn, cur = mysql_conn_as_root()
    try:
        cur.execute(sql)
        rows = cur.fetchall()
        if rows:
            print("\n" + sql)
            for row in rows:
                print(row)
        else:
            print("No result from query ", sql)
    except (mysql.connector.Error, mysql.connector.Warning) as e:
        print("MySQL error ", e)
    finally:
         cur.close()
         conn.close()
    #('mysql',)
    #('information_schema',)
    #('performance_schema',)
    #('sys',)

    # Grant all permissions on all databases and their tables to a user
    sql = """Grant all on *.* to markwkiehl@localhost;"""
    # Grant permissions to a specific database and its tables to a specified user
    sql = """grant all privileges on mydbtst.* to markwkiehl@localhost;"""
    print("\n" + sql)
    conn, cur = mysql_conn_as_root()
    try:
        cur.execute(sql)
        # No result returned
    except (mysql.connector.Error, mysql.connector.Warning) as e:
        print("MySQL error ", e)
    finally:
         cur.close()
         conn.close()

    sql = """Show grants for markwkiehl@localhost;"""
    print("\n" + sql)
    conn, cur = mysql_conn_as_user()
    try:
        cur.execute(sql)
        rows = cur.fetchall()
        if rows:
            for row in rows:
                print(row)
        else:
            print("No result from query ", sql)
    except (mysql.connector.Error, mysql.connector.Warning) as e:
        print("MySQL error ", e)
    finally:
         cur.close()
         conn.close()
    # ('GRANT USAGE ON *.* TO `markwkiehl`@`localhost`',)


    # Get the current user
    conn, cur = mysql_conn_as_user()
    sql = """SELECT user();"""
    try:
        cur.execute(sql)
        row = cur.fetchone()
        if row:
            print("\nCurrent MySQL user:", row[0])
            # root@localhost
            # markwkiehl@localhost
        else:
            print("No result from query")
    except (mysql.connector.Error, mysql.connector.Warning) as e:
        print("MySQL error ", e)
    finally:
         cur.close()
         conn.close()


    # Get the currently selected database
    sql = """SELECT DATABASE();"""
    conn, cur = mysql_conn_as_user()
    # Select a database to use
    # *** BELOW DOES NOT WORK ***
    #sql = """USE mydbtst;"""
    # Use method below to select a database  (or specifiy it in the db connection)
    conn.database = "mydbtst"
    try:
        cur.execute(sql)
        row = cur.fetchone()
        if row:
            print("\n'" + str(row[0]) + "' currently selected database")
        else:
            print("No result from query")
    except (mysql.connector.Error, mysql.connector.Warning) as e:
        print("MySQL error ", e)
    finally:
         cur.close()
         conn.close()
    # NOTE: The selected database using conn.database= only persists while conn is open.



    sql = """CREATE TABLE testtmp (id INT AUTO_INCREMENT PRIMARY KEY, 
            firstname VARCHAR(255), 
            lastname VARCHAR(255), 
            age INT NOT NULL,
            birth_date DATE NOT NULL,
            start_utc DATETIME,
            rec_created TIMESTAMP,
            cost DECIMAL(10,2),
            my_float FLOAT,
            my_double DOUBLE PRECISION
            ) ENGINE=InnoDB;"""
    # firstname,lastname,age,birth_date,start_utc,rec_created,cost,my_float,my_double
    print("\n" + sql)
    conn, cur = mysql_conn_as_user()
    conn.database = "mydbtst"
    try:
        cur.execute(sql)
        # No result returned
    except (mysql.connector.Error, mysql.connector.Warning) as e:
        print("MySQL error ", e)
    finally:
         cur.close()
         conn.close()

    sql = """SHOW TABLES;"""
    print("\n" + sql)
    conn, cur = mysql_conn_as_user()
    # NOTE: Must 'USE', select, or assign a database before attempting to work with a table
    conn.database = "mydbtst"
    try:
        cur.execute(sql)
        rows = cur.fetchall()
        if rows:
            for row in rows:
                print(row)
        else:
            print("No result from query ", sql)
    except (mysql.connector.Error, mysql.connector.Warning) as e:
        print("MySQL error ", e)
    finally:
         cur.close()
         conn.close()

    sql = """SELECT TABLE_NAME,ENGINE FROM information_schema.TABLES WHERE TABLE_SCHEMA = 'mydbtst';"""
    print("\n" + sql)
    conn, cur = mysql_conn_as_user()
    try:
        cur.execute(sql)
        rows = cur.fetchall()
        if rows:
            for row in rows:
                print(row)
        else:
            print("No result from query ", sql)
    except (mysql.connector.Error, mysql.connector.Warning) as e:
        print("MySQL error ", e)
    finally:
         cur.close()
         conn.close()


    sql = """SHOW TABLE STATUS FROM mydbtst;"""
    print("\n" + sql)
    conn, cur = mysql_conn_as_user()
    try:
        cur.execute(sql)
        rows = cur.fetchall()
        if rows:
            for row in rows:
                print(row)
        else:
            print("No result from query ", sql)
    except (mysql.connector.Error, mysql.connector.Warning) as e:
        print("MySQL error ", e)
    finally:
         cur.close()
         conn.close()


    # Show the table structure.
    sql = """DESCRIBE mydbtst.testtmp;"""
    print("\n" + sql)
    conn, cur = mysql_conn_as_user()
    #conn.database = "mydbtst"
    try:
        cur.execute(sql)
        rows = cur.fetchall()
        if rows:
            for row in rows:
                print(row)
        else:
            print("No result from query ", sql)
    except (mysql.connector.Error, mysql.connector.Warning) as e:
        print("MySQL error ", e)
    finally:
         cur.close()
         conn.close()


    sql = """INSERT INTO testtmp (firstname,lastname,age,birth_date,start_utc,rec_created,cost,my_float,my_double) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s);"""
    vals = ("Louise","Kiehl",66,"1958-09-07","2024-05-26 17:32:01","2024-05-26 17:32:01",-1234567.89,1.175494351E-38,-1.7976931348623157E+307)
    # firstname,lastname,age,birth_date,start_utc,rec_created,my_float,my_double
    print("\n" + sql)
    print(vals)
    conn, cur = mysql_conn_as_user()
    conn.database = "mydbtst"
    try:
        cur.execute(sql, vals)
        row = cur.fetchone()
        conn.commit()     # IMPORTANT! 
        # NOTE: Alt to .commit() is .rollback()
        print(cur.rowcount, "rows inserted")
        # 1 rows inserted
    except (mysql.connector.Error, mysql.connector.Warning) as e:
        print("MySQL error ", e)
    finally:
         cur.close()
         conn.close()

    sql = """SELECT * FROM mydbtst.testtmp ORDER BY id;"""
    print("\n" + sql)
    conn, cur = mysql_conn_as_user()
    try:
        cur.execute(sql)
        rows = cur.fetchall()
        if rows:
            for row in rows:
                print(row)
        else:
            print("No result from query ", sql)
    except (mysql.connector.Error, mysql.connector.Warning) as e:
        print("MySQL error ", e)
    finally:
         cur.close()
         conn.close()


    # REPAIR A TABLE
    # REPAIR TABLE only works with MyISAM engine, so must alter the table first
    sql = """ALTER TABLE mydbtst.testtmp ENGINE='MyISAM';"""
    print("\n" + sql)
    conn, cur = mysql_conn_as_user()
    try:
        cur.execute(sql)
        # No result returned
    except (mysql.connector.Error, mysql.connector.Warning) as e:
        print("MySQL error ", e)
    finally:
         cur.close()
         conn.close()
    sql = """REPAIR TABLE mydbtst.testtmp;"""
    print(sql)
    conn, cur = mysql_conn_as_user()
    try:
        cur.execute(sql)
        # No result returned
    except (mysql.connector.Error, mysql.connector.Warning) as e:
        print("MySQL error ", e)
    finally:
         #cur.close()
         conn.close()
    # ALTER TABLE mydbtst.testtmp ENGINE='InnoDB';
    sql = """ALTER TABLE mydbtst.testtmp ENGINE='InnoDB';"""
    print(sql)
    conn, cur = mysql_conn_as_user()
    try:
        cur.execute(sql)
        # No result returned
    except (mysql.connector.Error, mysql.connector.Warning) as e:
        print("MySQL error ", e)
    finally:
         cur.close()
         conn.close()


    #-----------------------------------------------------
    # CLEAN UP

    sql = """DROP TABLE IF EXISTS mydbtst.testtmp;"""
    # DROP TABLE  schema_name.table_name;  
    conn, cur = mysql_conn_as_user()
    #conn.database = "mydbtst"
    try:
        cur.execute(sql)
        # No result returned
    except (mysql.connector.Error, mysql.connector.Warning) as e:
        print("MySQL error ", e)
    finally:
         cur.close()
         conn.close()


    conn, cur = mysql_conn_as_root()
    sql = """DROP DATABASE IF EXISTS mydbtst;"""
    try:
        cur.execute(sql)
        # No result returned
    except (mysql.connector.Error, mysql.connector.Warning) as e:
        print("MySQL error ", e)
    finally:
         cur.close()
         conn.close()

    sql = """DROP USER IF EXISTS markwkiehl@localhost;"""
    conn, cur = mysql_conn_as_root()
    try:
        cur.execute(sql)
        # No result returned
    except (mysql.connector.Error, mysql.connector.Warning) as e:
        print("MySQL error ", e)
    finally:
         cur.close()
         conn.close()

    if mysql_user_exists('markwkiehl'): raise Exception("ERROR: MySQL user 'markwkiehl' still exists")

    print("\n")


if __name__ == '__main__':
    pass

    main()