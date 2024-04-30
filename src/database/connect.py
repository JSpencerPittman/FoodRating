import psycopg2
import re
from src.database.config import load_config


def connect(config):
    """ Connect to the PostgreSQL database server """
    try:
        # connecting to the PostgreSQL server
        with psycopg2.connect(**config) as conn:
            print('Connected to the PostgreSQL server.')
            return conn
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)

def extract_functions(sql_file):
    # Read the SQL file
    with open(sql_file, 'r') as f:
        sql_content = f.read()

    # Use regular expressions to extract function definitions
    pattern = r'CREATE OR REPLACE FUNCTION\s+(\w+)\s*\(([\s\S]*?)\)\s*RETURNS\s*([\s\S]*?)\s*AS\s*\$\$([\s\S]*?)\$\$\s*LANGUAGE\s*(\w+)\s*;'
    matches = re.findall(pattern, sql_content)

    # Extracted functions will be stored in a dictionary
    extracted_functions = {}
    
    # Iterate over the matches and populate the dictionary
    for match in matches:
        function_name = match[0]
        parameters = match[1].strip()
        return_type = match[2].strip()
        function_body = match[3].strip()
        language = match[4]

        # Create a function signature based on the parameters and return type
        signature = f'{function_name}({parameters}) -> {return_type}'
        
        # Store the function signature and body in the dictionary
        extracted_functions[signature] = function_body

    return extracted_functions

def create_python_functions(extracted_functions):
    python_functions = {}
    for signature, body in extracted_functions.items():
        # Define Python functions dynamically
        exec(f"def {signature}:\n{body}\n")
        python_functions[signature] = locals()[signature]
    return python_functions



if __name__ == '__main__':
    config = load_config()
    connect(config)
    sql_file = 'Rating.sql'
    functions = extract_functions(sql_file)
    python_functions = create_python_functions(functions)
    # Now you can use the extracted Python functions in your code
    print(python_functions.keys())  # Display the names of all extracted functions
       
       # Sample code to call a sql function in python
       # function_name = 'your_function_name'
       # if function_name in python_functions:
       # result = python_functions[function_name]()
