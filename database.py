#import libraries
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os
from pymysql.constants import CLIENT

#Initialize load_dotenv
load_dotenv()

#Create database url to connect vs code to mysql
db_hostname = os.getenv("db_username")
db_password = os.getenv("db_password")
db_host = os.getenv("db_host")
db_port = os.getenv("db_port")
db_name = os.getenv("db_name")

db_url = f"mysql+pymysql://{db_hostname}:{db_password}@{db_host}:{db_port}/{db_name}"

engine = create_engine(db_url, connect_args = {"client_flag": CLIENT.MULTI_STATEMENTS})

session = sessionmaker(bind = engine)
db = session()

#Test connection
with session() as f:
    print(f.execute(text("select version();")).fetchone())

create_query = text("""
        create table if not exists employees(
                    id int primary key auto_increment,
                    name varchar(100) not null, 
                    email varchar(100) unique not null,
                    password varchar(255) not null,
                    position varchar(100),
                    department varchar(100), 
                    date_hired date,
                    salary decimal(10, 2),
                    is_active bool default true
                    );
""")


print("Table created sucessfully")


fill_table = text("""
            insert into employees(name, email, password, position, department, date_hired, salary) values
                  ("David Ekpo", "davidekpo100@gmail.com", "cool", "CFO", "Finance", "2023-05-10", 15000000);
""")
if __name__ == "__main__":
    db.execute(create_query)
    db.execute(fill_table)
    db.commit()