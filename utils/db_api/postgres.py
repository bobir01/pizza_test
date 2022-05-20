import json
from operator import truediv
from textwrap import indent
from typing import Union

import asyncpg
from asyncpg import Connection
from asyncpg.pool import Pool

from data import config

class Database:

    def __init__(self):
        self.pool: Union[Pool, None] = None

    async def create(self):
        self.pool = await asyncpg.create_pool(
            user=config.DB_USER,
            password=config.DB_PASS,
            host=config.DB_HOST,
            database=config.DB_NAME
        )

    async def execute(self, command, *args,
                      fetch: bool = False,
                      fetchval: bool = False,
                      fetchrow: bool = False,
                      execute: bool = False
                      ):
        async with self.pool.acquire() as connection:
            connection: Connection
            async with connection.transaction():
                if fetch:
                    result = await connection.fetch(command, *args)
                elif fetchval:
                    result = await connection.fetchval(command, *args)
                elif fetchrow:
                    result = await connection.fetchrow(command, *args)
                elif execute:
                    result = await connection.execute(command, *args)
            return result

    async def create_table_users(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Users (
        id SERIAL PRIMARY KEY,
        full_name VARCHAR(255) NOT NULL,
        username varchar(255) NULL,
        telegram_id BIGINT NOT NULL UNIQUE 
        );
        """
        await self.execute(sql, execute=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ${num}" for num, item in enumerate(parameters.keys(),
                                                          start=1)
        ])
        return sql, tuple(parameters.values())

    async def add_user(self, full_name, username, telegram_id):
        sql = "INSERT INTO users (full_name, username, telegram_id) VALUES($1, $2, $3) returning *"
        return await self.execute(sql, full_name, username, telegram_id, fetchrow=True)

    async def select_all_users(self):
        sql = "SELECT * FROM Users"
        return await self.execute(sql, fetch=True)

    async def select_user(self, **kwargs):
        sql = "SELECT * FROM Users WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)

    async def count_users(self):
        sql = "SELECT COUNT(*) FROM Users"
        return await self.execute(sql, fetchval=True)

    async def update_user_username(self, username, telegram_id):
        sql = "UPDATE Users SET username=$1 WHERE telegram_id=$2"
        return await self.execute(sql, username, telegram_id, execute=True)

    async def delete_users(self):
        await self.execute("DELETE FROM Users WHERE TRUE", execute=True)

    async def drop_users(self):
        await self.execute("DROP TABLE Users", execute=True)

#----------------------------SQL PRODUCTS------------------------------------------------------------------------------
    async def create_products_table(self):
        sql="""
            CREATE TABLE IF NOT EXISTS products (
                id  SERIAL PRIMARY KEY,
                category VARCHAR(100) NOT NULL,
                item_name VARCHAR(200) NOT NULL,
                item_image VARCHAR(255) NOT NULL,
                description TEXT,
                item_price BIGINT NOT NULL,
                key_type VARCHAR(100)

            )"""
        await self.execute(sql, execute=True)

#      for inserting values in to db
    async def add_product(self, category, item_name,item_image, description, item_price, key_type):
        sql= """
            insert into products(category, item_name, item_image, description, item_price, key_type) values ($1,$2,$3,$4, $5, $6) returning *
        """
        return await self.execute(sql, category, item_name,item_image, description, item_price, key_type, fetchrow=True)

# for getting category from our db 

    async def select_category(self):
        sql="select DISTINCT category from products"
        return await self.execute(sql, fetch=True)

# for getting item_name where it belongs to category

    async def select_item(self, category:str):
        sql ="select item_name from products where category = $1 order by id "
        return await self.execute(sql ,category, fetch=True)

    # for getting item details from db correspondingly with item_name

    async def select_item_details(self, item_name:str):
        sql = "select item_image, description, item_price, key_type from products where item_name= $1 "
        return await self.execute(sql, item_name, fetchrow=True)


    
#----------------------- basket------------------------------


    async def create_table_basket(self):
        sql = """
        CREATE TABLE IF NOT EXISTS basket (
        id SERIAL PRIMARY KEY,
        full_name VARCHAR(255) NOT NULL,
        telegram_id BIGINT NOT NULL ,
        category VARCHAR(255) NULL,
        item_name VARCHAR(255) NULL,
        item_price bigint null,
        quantity bigint null,
        item_size varchar(20)
        );
        """
        await self.execute(sql, execute=True)


    async def add_to_basket(self,full_name ,telegram_id, category, item_name, item_price, quantity, item_size=None):
        sql_size= """
            insert into basket(full_name, telegram_id, category,  item_name, item_price, quantity, item_size) values ($1,$2,$3,$4, $5, $6, $7) returning *
        """
        sql= """
            insert into basket(full_name, telegram_id , category, item_name,  item_price, quantity) values ($1,$2,$3,$4, $5, $6) returning *
        """

        if item_size:
            return await self.execute(sql_size, full_name, telegram_id, category, item_name, item_price, quantity, item_size, fetchrow=True)
        else:
            return await self.execute(sql, full_name, telegram_id, category, item_name, item_price, quantity, fetchrow=True)



    async def select_basket(self, telegram_id):
        sql ="select item_name, category, item_price, quantity from basket where telegram_id = $1 order by id "
        return await self.execute(sql ,telegram_id, fetch=True)

    
    async def select_basket_item(self, telegram_id):
        sql ="select id, item_name, item_price, quantity, item_size from basket where telegram_id = $1 order by id "
        return await self.execute(sql ,telegram_id, fetch=True)

    async def emty_basket(self, telegram_id):
        sql ="delete from basket where telegram_id = $1"
        return await self.execute(sql ,telegram_id, execute=True)

    async def update_basket_quantity(self,item_id, action):
        sql_plus = "update basket set quantity=quantity+1 where id = $1"
        sql_minus= "update basket set quantity=quantity-1 where id = $1"
        if action=="-":
            return await self.execute(sql_minus, item_id, execute=True)
        else:
            return await self.execute(sql_plus, item_id, execute=True)

    async def delete_basket_item(self,item_id):
        sql = "delete from basket where id = $1"
        return await self.execute(sql, item_id, execute=True)


    async def create_table_history(self):
        sql = "CREATE TABLE IF NOT EXISTS purchase_history("\
              "id SERIAL PRIMARY KEY,"\
              "user_telegram_id BIGINT NOT NULL,"\
              "purchased_time TIMESTAMP,"\
              "json TEXT NOT NULL);"

        await self.execute(sql, execute=True)

    async def add_to_history(self, telegram_id, time_stamp, json_str):
        sql = "insert into purchase_history(user_telegram_id, purchased_time, json) values($1,$2,$3) returning *"
        await self.execute(sql, telegram_id, time_stamp, json_str, execute=True)

    async def get_all_history(self, telegram_id):
        sql = "select * from purchase_history where user_telegram_id "
        return await self.execute(sql, telegram_id, fetch=True)

    async def get_history_json(self, telegram_id):
        sql = "select json from purchase_history where user_telegram_id = $1"
        data = {}
        json_items = await self.execute(sql, telegram_id, fetch=True)
        # for index, item in  enumerate(json_items, start=1):
        #     user_json = json.loads(item[0] if len(item)>=1 else item)
        #     data[index] = user_json

        return json_items

    
