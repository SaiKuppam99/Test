import json

# Function to generate and execute SQL statements for permissions
def grant_permissions(users_data):
    for user_data in users_data:
        username = user_data['username']
        permissions = user_data['permissions']
        
        # Iterate through permissions for each database
        for db_name, db_permissions in permissions.items():
            # If db_permissions is a list, grant permissions at the database level
            if isinstance(db_permissions, list):
                for action in db_permissions:
                    sql_statement = f"GRANT {action} ON `{db_name}`.* TO '{username}'@'%'"
                    print(f"Executing SQL: {sql_statement}")
                    # Execute the SQL statement in your database management system
            # If db_permissions is a dictionary, handle table-level permissions
            elif isinstance(db_permissions, dict):
                for table_name, table_actions in db_permissions.items():
                    for action in table_actions:
                        sql_statement = f"GRANT {action} ON `{db_name}`.`{table_name}` TO '{username}'@'%'"
                        print(f"Executing SQL: {sql_statement}")
                        # Execute the SQL statement in your database management system

# Call the function to grant permissions
grant_permissions(users_data)
