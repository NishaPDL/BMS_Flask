from peewee import PostgresqlDatabase


DATABASE = {
    'name': 'nbfc_db',
    'user': 'nbfc_user',
    'password': 'nbfc_pass',
    'host': 'localhost',
    'port': 5432
}

db = PostgresqlDatabase(
    DATABASE['name'], 
    user=DATABASE['user'], 
    password=DATABASE['password'], 
    host=DATABASE['host'], 
    port=DATABASE['port']
)
