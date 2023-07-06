pip install boto3 pymysql

import boto3

def create_aurora_user(db_cluster_identifier, username, password, db_name, table_name):
    # Create an RDS client
    client = boto3.client('rds')

    # Create the user
    response = client.create_db_instance(
        DBInstanceIdentifier=db_cluster_identifier,
        MasterUsername=username,
        MasterUserPassword=password,
        Engine='aurora',
        DBInstanceClass='db.r5.large',
        Port=3306,
        DBClusterIdentifier=db_cluster_identifier,
        EngineMode='provisioned',
        AllocatedStorage=20
    )

    # Wait for the DB instance to become available
    waiter = client.get_waiter('db_instance_available')
    waiter.wait(DBInstanceIdentifier=db_cluster_identifier)

    # Connect to the database
    import pymysql

    host = response['DBInstance']['Endpoint']['Address']
    connection = pymysql.connect(host=host, user=username, password=password, database=db_name)

    # Grant database-level privileges
    cursor = connection.cursor()
    cursor.execute(f"GRANT ALL PRIVILEGES ON {db_name}.* TO '{username}'@'%'")
    cursor.execute("FLUSH PRIVILEGES")

    # Grant table-level privileges
    cursor.execute(f"GRANT ALL PRIVILEGES ON {db_name}.{table_name} TO '{username}'@'%'")
    cursor.execute("FLUSH PRIVILEGES")

    # Close the connection
    cursor.close()
    connection.close()

    print(f"User '{username}' created and granted access to database '{db_name}' and table '{table_name}'")

# Usage
create_aurora_user('my-db-cluster', 'new_user', 'new_password', 'my_database', 'my_table')
