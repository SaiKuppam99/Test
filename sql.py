import json

def generate_sql_statements_from_file(file_path):
    with open(file_path, 'r') as json_file:
        users_data = json.load(json_file)

    sql_statements = []

    for user_data in users_data:
        username = user_data['username']
        permissions = user_data['permissions']

        for db_name, table_permissions in permissions.items():
            if db_name == "*":
                db_name = "*.*"
                if isinstance(table_permissions, list):
                    for action in table_permissions:
                        sql_statement = f"GRANT {action} ON {db_name} TO '{username}'@'%';"
                        sql_statements.append(sql_statement)
            else:
                db_name = f"`{db_name}`"
                if isinstance(table_permissions, dict):
                    for table_name, actions in table_permissions.items():
                        if table_name == "*":
                            table_name = "*.*"
                            for action in actions:
                                sql_statement = f"GRANT {action} ON {db_name}.{table_name} TO '{username}'@'%';"
                                sql_statements.append(sql_statement)
                        else:
                            table_name = f"`{table_name}`"
                            for action in actions:
                                sql_statement = f"GRANT {action} ON {db_name}.{table_name} TO '{username}'@'%';"
                                sql_statements.append(sql_statement)

    return sql_statements

def execute_sql_statements(sql_statements, db_host, db_user, db_password, db_name):
    try:
        connection = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_name
        )

        if connection.is_connected():
            cursor = connection.cursor()

            for statement in sql_statements:
                cursor.execute(statement)
                print(f"Executed: {statement}")

            connection.commit()

    except mysql.connector.Error as error:
        print(f"Error: {error}")

    finally:
        # Close the cursor and connection
        if 'cursor' in locals() and cursor is not None:
            cursor.close()
        if 'connection' in locals() and connection.is_connected():
            connection.close()
            print("Database connection closed.")

# Example usage:
json_file_path = 'path/to/your/json/file.json'
sql_statements = generate_sql_statements_from_file(json_file_path)

for statement in sql_statements:
    print(statement)
