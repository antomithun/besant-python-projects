import mysql.connector

# Establish a connection to the MySQL database
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="12345",
    database="corona_db"  # Change the database name to your specific corona database
)

# Create a cursor object to interact with the database
mycursor = mydb.cursor()

# Define the SQL queries to create tables
create_death_details_table = """
CREATE TABLE IF NOT EXISTS death_details (
    id INT AUTO_INCREMENT PRIMARY KEY,
    person_name VARCHAR(255) NOT NULL,
    date_of_death DATE,
    cause_of_death VARCHAR(255)
)
"""

create_vaccinated_details_table = """
CREATE TABLE IF NOT EXISTS vaccinated_details (
    id INT AUTO_INCREMENT PRIMARY KEY,
    person_name VARCHAR(255) NOT NULL,
    vaccination_date DATE,
    vaccine_type VARCHAR(255),
    vaccine_dose INT
)
"""

create_not_vaccinated_details_table = """
CREATE TABLE IF NOT EXISTS not_vaccinated_details (
    id INT AUTO_INCREMENT PRIMARY KEY,
    person_name VARCHAR(255) NOT NULL,
    reason VARCHAR(255)
)
"""

# Execute the SQL queries to create the tables
mycursor.execute(create_death_details_table)
mycursor.execute(create_vaccinated_details_table)
mycursor.execute(create_not_vaccinated_details_table)

# Commit the changes to the database
mydb.commit()

# Close the cursor and database connection
mycursor.close()
mydb.close()

print("Tables created successfully!")
# Function to insert data into a table
def insert_data(table_name, column_names, values):
    try:
        # Prepare the SQL query
        sql = f"INSERT INTO {table_name} ({', '.join(column_names)}) VALUES ({', '.join(['%s'] * len(values))})"
        
        # Execute the SQL query with the provided values
        mycursor.execute(sql, values)
        
        # Commit the changes to the database
        mydb.commit()
        
        print(f"Data inserted into {table_name} successfully!")
    except Exception as e:
        print(f"Error inserting data: {str(e)}")

# Function to view data from a table
def view_data(table_name):
    try:
        # Execute a SELECT query to retrieve data from the table
        mycursor.execute(f"SELECT * FROM {table_name}")
        
        # Fetch all rows of data
        result = mycursor.fetchall()
        
        # Display the data
        for row in result:
            print(row)
    except Exception as e:
        print(f"Error viewing data: {str(e)}")

# Function to update data in a table
def update_data(table_name, column_to_update, new_value, condition_column, condition_value):
    try:
        # Prepare the SQL query for updating data
        sql = f"UPDATE {table_name} SET {column_to_update} = %s WHERE {condition_column} = %s"
        
        # Execute the SQL query with the provided values
        mycursor.execute(sql, (new_value, condition_value))
        
        # Commit the changes to the database
        mydb.commit()
        
        print("Data updated successfully!")
    except Exception as e:
        print(f"Error updating data: {str(e)}")

# Function to delete data from a table
def delete_data(table_name, column_name, value):
    try:
        # Prepare the SQL query for deleting data
        sql = f"DELETE FROM {table_name} WHERE {column_name} = %s"
        
        # Execute the SQL query with the provided value
        mycursor.execute(sql, (value,))
        
        # Commit the changes to the database
        mydb.commit()
        
        print("Data deleted successfully!")
    except Exception as e:
        print(f"Error deleting data: {str(e)}")

# Main function for managing the corona database
def main_function():
    print("****Corona Database Management****")
    print("1 -> Insert data")
    print("2 -> View data")
    print("3 -> Update data")
    print("4 -> Delete data")
    
    user = input("Enter your choice (1/2/3/4): ")
    
    if user == '1':
        table_name = input("Enter table name (e.g., death_details, vaccinated_details, not_vaccinated_details, not_affected_person_details): ")
        column_names = input("Enter column names separated by commas: ").split(',')
        values = input("Enter values separated by commas: ").split(',')
        insert_data(table_name.strip(), [col.strip() for col in column_names], [val.strip() for val in values])
    elif user == '2':
        table_name = input("Enter table name to view: ")
        view_data(table_name.strip())
    elif user == '3':
        table_name = input("Enter table name to update: ")
        column_to_update = input("Enter column name to update: ")
        new_value = input("Enter new value: ")
        condition_column = input("Enter condition column name: ")
        condition_value = input("Enter condition value: ")
        update_data(table_name.strip(), column_to_update.strip(), new_value.strip(), condition_column.strip(), condition_value.strip())
    elif user == '4':
        table_name = input("Enter table name to delete from: ")
        column_name = input("Enter column name to specify the deletion: ")
        value = input(f"Enter value to delete in {column_name} column: ")
        delete_data(table_name.strip(), column_name.strip(), value.strip())
    else:
        print("Please enter a valid choice (1/2/3/4)")

# Start the program
main_function()
