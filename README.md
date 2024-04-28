# NLSQL

Generates SQL query from natural language for your PostrgreSQL database. 
Simply connects to your database, gets the schema and generates query appropriately.

## User Guide

you can use nlsql as httpserver and as a cli-command

## nlsql as http server
1. start up the api server
	```bash
	python main.py -s
	```
2. get results via curl
	```curl
	curl --location 'http://localhost:8000/query/' \
	--header 'Content-Type: application/json' \
	--data-raw '{
	"question": "get users with post that has top views and top reactions in the last 24 hours",
	"db_url": "postgresql://postgres:postgres@localhost:5432/postgres"
	}'
	```

## nlsql as cli command

```bash
python main.py -m "./Nous-Hermes-2-Mistral-7B-DPO.Q4_0.gguf" -d "postgresql://postgres:postgres@localhost:5432/postgres" -q "get users with post that has top views and top reactions in the last 24 hours"
```
## Response
```sql
    SELECT DISTINCT ON (users.id) users.id, users.name
    FROM users
    JOIN posts ON users.id = posts.post_creator_user_id
    WHERE posts.created_at > now() - interval '1 day'
    GROUP BY users.id, users.name
    HAVING SUM(posts.views) >= ALL (SELECT SUM(views) FROM posts WHERE created_at > now() - interval '1 day') AND SUM(posts.reactions) >= ALL (SELECT SUM(reactions) FROM posts WHERE created_at > now() - interval '1 day');
```

response was generated over the following `users` and `posts` tables:
```
postgres=# \d users
   Column   |            Type             | Collation | Nullable |              Default              
------------+-----------------------------+-----------+----------+-----------------------------------
 id         | integer                     |           | not null | nextval('users_id_seq'::regclass)
 name       | text                        |           |          | 
 created_at | timestamp without time zone |           |          | 

postgres=# \d posts
        Column        |            Type             | Collation | Nullable |              Default              
----------------------+-----------------------------+-----------+----------+-----------------------------------
 id                   | integer                     |           | not null | nextval('posts_id_seq'::regclass)
 title                | text                        |           |          | 
 url                  | text                        |           |          | 
 post_creator_user_id | integer                     |           |          | 
 views                | integer                     |           |          | 
 reactions            | integer                     |           |          | 
 created_at           | timestamp without time zone |           |          | 
 updated_at           | timestamp without time zone |           |          | 

 ```
