# Datamaker

Rapidly build tabular datasets in the following formats:
- SQL Tables (Generate code for SQL CREATE and INSERT queries)
- CSV 
- JSON

Supports: PostgreSQL, MySQL, MS SQL, SQLite

## Getting Started
Datamaker uses core python 3 and has been extensively tested on python 3.6+. 

### Prerequisites
Python 3.6+

### Installing
```pip install datamaker```

### Build a dataset
In this example we build a SQL table with 50 rows and two columns: id, name. The create and 
insert queries will be written to the file example.sql.
```
from datamaker.SQLTableGenerator import SQLTableGen


table_name = "Example"
num_rows = 50
column_defs = {
    "id": {"col_type": "int", "is_primary_key": True},
    "name": {"col_type": "varchar", "is_name": True}
}
output_path = "example.sql"

gen = SQLTableGen(table_name, num_rows, column_defs, output_path)

gen.build_sql_doc()
```

## Documentation
### Input parameters
- **table_name**  - This is the name of the table to be created
- **num_rows** - The number of rows to insert into the table
- **column_defs** - A dictionary object with key value pairs.
- **path** - The path to the directory and file name where you want to export the sql
queries or dataset for the specified format.

**column_defs** is a dictionary object of the form:
```
{column_name: {"col_type": type, ...}}
```
Note that col_type is always specified for each column. The definitions of the parameters for **colum_defs** is given 
below.

- col_type: int, float, varchar, bool
- varchar_length: int (required for MySQL and MS SQL)
- is_primary_key: bool - True if this field is the primary key
- is_name: bool - True if values for this column should come from the names collection
- is_email: bool - True if this column is an email. Note that you must have at least one column with is_name = True 
to use is_email.
- is_date: bool - True if this column is a date. Default format is YYYY-mm-dd
- is_timestamp: bool - True if this column is a timestamp. Default format is YYYY-mm-dd HH:MM:SS
- is_country: bool - True of this column is a country code. Codes are ISO Alpha-2.
- is_state: bool - True if this column is a US state abbreviation. 
- is_address: bool - True if this column is a street address.
- bounds: tuple(lowerbnd, upperbnd) - Forces lowerbnd <= column values <= upperbnd
- fixed_collection: tuple(elem1, elem2, ..., elemn) - Forces column values to be elements of this tuple
- fixed_map: tuple(column_name, {key: value}) - Forces values for this column to be associated to the value of another 
column
- is_nullable: bool - True if this column can have null values
- proportion_null: float - The approximate proportion of expected null values in this column. Note that is_nullable 
must be true to use proportion_null

Note that using is_primary_key assumes the column you're defining is an integer column starting at 1 and incrementing
by 1 for each row.

If you're planning on running queries on a MySQL or MS SQL Server machine then you
need to specify the length of each varchar field using the varchar_length parameter.

## CSV and JSON generators
Datamaker can also be used to generate CSV and JSON files.

To create a CSV file add the following import statement to your script.

```from datamaker.CSVGenerator import CSVGen```

And to create a JSON file add the following import to your script.

```from datamaker.JSONGenerator import JSONGen```


The input parameters are no different for CSVGen and JSONGen are the same as given above. If we want to create the 
**Example** table given in the example code above as a CSV or JSON document we only to change the import statement and 
instantiate the CSVGen or JSONGen object using the same column_defs dictionary. Then call the appropriate build method
for the given class. The CSVGen class uses ```build_csv_doc``` and the JSONGen class uses ```build_json_doc```.

```
from datamaker.CSVGenerator import CSVGen


table_name = "Example"
num_rows = 50
column_defs = {
    "id": {"col_type": "int", "is_primary_key": True},
    "name": {"col_type": "varchar", "is_name": True}
}
output_path = "example.csv"

gen = CSVGen(table_name, num_rows, column_defs, output_path)

gen.build_csv_doc()
```

Here's the same **Example** table built as a JSON document.

```
from datamaker.JSONGenerator import JSONGen


table_name = "Example"
num_rows = 50
column_defs = {
    "id": {"col_type": "int", "is_primary_key": True},
    "name": {"col_type": "varchar", "is_name": True}
}
output_path = "example.json"

gen = JSONGen(table_name, num_rows, column_defs, output_path)

gen.build_json_doc()
```

## A more complex example
In this example we're generating SQL code to create a MySQL table which tracks orders placed for an imaginary online 
store. We'll create a table with the following columns:
- id - the primary key for this table
- name - the name associated to the user who placed this order
- order_ts - the timestamp associated with this order
- product_id - the id for the product ordered
- price - the cost of the product being ordered. Since we want every row with a given product_id to have the same cost we 
use a fixed map to implement this column 

Note that in this example we're defining the output path as a valid directory instead of a path to a file. In this 
case datamaker will automatically generate the name of the file as: 

**table_name**.**current_date**.sql

Where **table_name** is the name of the table and **current_date** is today's date.

```
from datamaker.SQLTableGenerator import SQLTableGen


table_name = "Orders"
num_rows = 500
column_defs = {
    "id": {"col_type": "int", "is_primary_key": True},
    "name": {"col_type": "varchar", "varchar_length": 50, "is_name": True},
    "order_ts": {"col_type": "varchar", "varchar_length": 26, "is_timestamp": True},
    "product_id": {"col_type": "int", "bounds": (1, 5)},
    "price": {"col_type": "float", "fixed_map": ("product_id", {1: 5.99, 2: 10.99, 3: 0.99, 4: 99.99, 5: 20})},
}
output_path = "."

gen = SQLTableGen(table_name, num_rows, column_defs, output_path)

gen.build_sql_doc()
```

### Future improvements:
- Add support for sequential fields
- Add support for column type inference
- Add support for tsv generation
