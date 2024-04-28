## Usage

```
usage: main.py [-h] -m MODEL_PATH -d DB_URL -q QUESTION

Convert natural language into SQL query

options:
  -h, --help            show this help message and exit
  -m MODEL_PATH, --model-path MODEL_PATH
                        Path to the model file (in gguf format), if not provided it uses groq api for inference
  -d DB_URL, --db-url DB_URL
                        PostgreSQL database URL link
  -q QUESTION, --question QUESTION
                        Question to generate a SQL query
  -s, --server          Serve nlsql as http server
```
