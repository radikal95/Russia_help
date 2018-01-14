import telebot
import config
from db_tool import DbQuery
db_query = DbQuery()

query = """SELECT full_name,auth,id
	        FROM "user";"""
query_result=db_query.execute_query(query)
print(query_result.success)
