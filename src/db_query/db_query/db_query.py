import pymysql
import json
from aws_lambda_powertools import Logger

logger = Logger()



class DatabaseQuery:
    def __init__(self, credentials):
        self.credentials = credentials

    def execute_query(self, query_template, query_params):
        # Extract credentials
        db_username = self.credentials['db_username']
        db_password = self.credentials['db_password']
        db_name = self.credentials['db_name']
        db_host = self.credentials['db_host']

        try:
            # Establish the database connection
            connection = pymysql.connect(
                host=db_host,
                user=db_username,
                password=db_password,
                database=db_name,
                connect_timeout=10
            )
            logger.info(f"Connected to the database '{db_name}' successfully.")

            # Execute the provided query with the given parameters
            with connection.cursor() as cursor:
                logger.info(f"Executing SQL query: {query_template} with params {query_params}")
                cursor.execute(query_template, query_params)
                result = cursor.fetchone()

                if result:
                    logger.info(f"Query result: {result}")
                    # Return the result as a JSON string
                    return json.dumps(dict(zip([desc[0] for desc in cursor.description], result)))
                else:
                    logger.warning("No results found.")
                    return 'no_results'

        except pymysql.MySQLError as e:
            logger.error(f"Error querying the database: {e}")
            return 'error'

        finally:
            # Ensure the connection is closed
            if 'connection' in locals():
                connection.close()
                logger.info("Database connection closed.")
