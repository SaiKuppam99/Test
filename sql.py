def generate_sql_statements(users_data):
    sql_statements = []
    
    for user_data in users_data:
        username = user_data['username']
        permissions = user_data['permissions']
        
        for db_name, table_permissions in permissions.items():
            if db_name == "*":
                db_name = "*.*"
            else:
                db_name = f"`{db_name}`"
                
            if isinstance(table_permissions, list):
                # Permissions for all tables in the database
                table_permissions = "*"
            
            for table_name, actions in table_permissions.items():
                if table_name == "*":
                    table_name = "*.*"
                else:
                    table_name = f"`{db_name}`.`{table_name}`"
                
                for action in actions:
                    sql_statement = f"GRANT {action} ON {table_name} TO '{username}'@'%';"
                    sql_statements.append(sql_statement)
    
    return sql_statements


sql_statements = generate_sql_statements(users_data)
for statement in sql_statements:
    print(statement)
