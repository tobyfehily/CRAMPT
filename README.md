# Chemist Warehouse Retail Aisle Minimum Parameter Tracker (CRAMPT)


## Links
[GitHub repository](https://github.com/tobyfehily/CRAMPT)


## Identification of the problem you are trying to solve by building this particular app.
Chemist Warehouse is an Australian retail pharmacy chain with more than 500 stores and over $3 billion in sales in 2022. 

There is anecdotal evidence, e.g., from customer reports on social media, that the aisles at Chemist Warehouse outlets are too narrow:

>Honestly! The aisles at Chemist Warehouse are so narrow that every trip feels like a rebirth[...] _- DF_

>i really hate how narrow the aisles are at chemist warehouse _- alaa_

>i can't deal with chemist warehouse, its too cluttered and the aisles are too narrow, just go away you damn store _- rachelp2134_

However, there is currently no readily available data about Chemist Warehouse aisle widths for customers. 

The Chemist Warehouse Retail Aisle Minimum Parameter Tracker (CRAMPT) offers a robust, scalable solution for both crowd-sourcing this neglected datapoint and making it easily accessible to customers.


## Why is it a problem that needs solving?
Narrow aisle widths present challenges for many people. This includes disabled people, visually impaired people, wheelchair users, pram users, people with anxiety, and neurodivergent people. Compounding the problem is the fact that those most adversely affected by narrow aisle widths may be in greater need of retail pharmacy services. 

An Australian Network on Disability (AND) survey of 298 disabled people rated "aisle width and room to move around" as the third-most important attribute of in-store experiences. And yet despite accessibility provisions in the National Construction Code and Building Code of Australia, minimum corridor width requirements are not always upheld.

By potentially failing to cater to a significant customer base, business such as Chemist Warehouse may be missing out on profits. More importantly, neglecting to provide accessible goods and services is illegal in Australia, considered discrimination under the _Disability Discrimination Act 1992_ (Cth).

A lack of data about aisle widths at Chemist Warehouse outlets is one small, solvable part of a much larger problem. There is also a general lack of awareness about accessibility needs in Australia more broadly. Through its focused niche, CRAMPT encourages a more far-reaching conversation about accessibility.


## Why have you chosen this database system. What are the drawbacks compared to others?
PostgreSQL is a well-known database management system (DBMS) commonly used in web applications. It is currently the second-most-used DBMS, after MySQL, having almost tripled in popularity in the last eight years. Its strong performance is reflected by the number of top companies using it, which include Apple, IMDb, Instagram, Reddit, Skype, Spotify and Twitch.

Its advantages include its free and open source status, obviating expensive licensing fees and making the most of active community contributions and support. PostgreSQL supports a wide range of popular programming languages and protocols such as Python, Java, Perl, .Net, Go, Ruby, C/C++, Tcl and ODBC (AWS) – more than other popular DBMSs, like MySQL (Ravoof 2023). It is also considered the most security-aware database available, which is important when handling sensitive information such as email addresses and passwords, authenticating users, and authorising admin permissions.

PostgreSQL offers unique benefits for CRAMPT due to the fact that it is an Object-Relational Database Management System, as opposed to a vanilla Relational Database Management System. This presents the potential for more flexibility and complexity by allowing for object-oriented programming-related concepts such as inheritance.

However, PostgreSQL's ability to handle complex queries can make installation and configuration challenging for beginners, compared to MySQL. Further, PostgreSQL runs slower for read-only commands compared to simpler, more lightweight DBMSs, such as MySQL. Given CRAMPT's need for complex queries, and the potential to further scale the database in the future (e.g., hooking into Chemist Warehouse store locator API, providing additional accessibility information, incorporating other stores), PostgreSQL's benefits far outweigh its drawbacks.


##	Identify and discuss the key functionalities and benefits of an ORM
An Object Relational Mapper (ORM), like SQLAlchemy, maps an object orienting programming (OOP) language, such as Python, to a relational database, such as SQL. It can be thought of as an interpreter, seamlessly translating between different languages. Moreover, it makes the most of OOP's power and adaptability while minimising the inherent complexities and redundancies of SQL queries.

The key features of an ORM include mapping OOP objects to relational database tables, including relationships between them (e.g., one-to-one, one-to-many, many-to-many), and allowing developers to query and manipulate relational database data by carrying out Create, Read, Update, Delete (CRUD) operations on the database through OOP code.

Its benefits include reduced code cruft and increased productivity, as developers do not need to get mired in SQL queries, as well as improved maintainability and extensibility, thanks to OOP's deft handling of abstraction, polymorphism, inheritance and encapsulation. ORMs also provide better security by offering additional opportunities to sanitise data and thereby protect from malicious attacks, such as SQL injections.


## Document all endpoints for your API

### /users
- **HTTP request verb**: GET
- **Required data where applicable**: N/A
- **Expected response data**: '200 OK', users excluding password, reports
- **Authentication methods where applicable**: Admin only (JWT bearer token authentication)

### /users/&lt;int:user_id&gt;
- **HTTP request verb**: PUT
- **Required data where applicable**: Email and password
- **Expected response data**: '200 OK', user email and password
- **Authentication methods where applicable**: Admin or associated user only (JWT bearer token authentication)

### /users/&lt;int:user_id&gt;
- **HTTP request verb**: DELETE
- **Required data where applicable**: N/A
- **Expected response data**: '200 OK', empty JSON string
- **Authentication methods where applicable**: Admin or associated user only (JWT bearer token authentication)

### /users/&lt;int:user_id&gt;/reports
- **HTTP request verb**: GET
- **Required data where applicable**: N/A
- **Expected response data**: '200 OK', reports, including aisle width, date created, id, image and store id
- **Authentication methods where applicable**: Admin or associated user only (JWT bearer token authentication)

### /users/register
- **HTTP request verb**: POST
- **Required data where applicable**: Email, password
- **Expected response data**: '201 created', user email, id
- **Authentication methods where applicable**: N/A

### /users/login>
- **HTTP request verb**: POST
- **Required data where applicable**: Email, password
- **Expected response data**: '200 OK', user email, id, JWT bearer token
- **Authentication methods where applicable**: N/A

### /stores
- **HTTP request verb**: GET
- **Required data where applicable**: N/A
- **Expected response data**: '200 OK', stores excluding reports
- **Authentication methods where applicable**: N/A

### /stores
- **HTTP request verb**: POST
- **Required data where applicable**: Name, address, suburb and state (optional: email, phone number, aisle width)
- **Expected response data**: '201 Created', store including id, name, address, suburb, state, email, phone number, aisle width
- **Authentication methods where applicable**: Admin only (JWT bearer token authentication)

### /stores/&lt;int:store_id&gt;
- **HTTP request verb**: PUT, PATCH
- **Required data where applicable**: Name, address, suburb, state, email, phone number or aisle width
- **Expected response data**: '200 OK', store including id, name, address, suburb, state, email, phone number and aisle width
- **Authentication methods where applicable**: Admin only (JWT bearer token authentication)

### /stores/&lt;int:store_id&gt;
- **HTTP request verb**: DELETE
- **Required data where applicable**: N/A
- **Expected response data**: '200 OK', empty JSON string
- **Authentication methods where applicable**: Admin only (JWT bearer token authentication)

### /stores/&lt;int:user_id&gt;/reports
- **HTTP request verb**: GET
- **Required data where applicable**: N/A
- **Expected response data**: '200 OK', reports, including aisle width, date created, id, image and store id
- **Authentication methods where applicable**: Admin only (JWT bearer token authentication)

### /stores/search?=&lt;int:aisle_width_min&gt;
- **HTTP request verb**: GET
- **Required data where applicable**: N/A
- **Expected response data**: '200 OK', stores with aisle width larger than `aisle_width_min`, including address, aisle width, email, store id, name, phone number, state and suburb
- **Authentication methods where applicable**: Admin only (JWT bearer token authentication)

### /reports
- **HTTP request verb**: GET
- **Required data where applicable**: N/A
- **Expected response data**: '200 OK', reports including aisle width, date created, id, image, store id, user id
- **Authentication methods where applicable**: Admin only (JWT bearer token authentication)

### /reports
- **HTTP request verb**: POST
- **Required data where applicable**: N/A
- **Expected response data**: '201 Created', reports including aisle width, date created, image, store id, report id
- **Authentication methods where applicable**: Admin or user only (JWT bearer token authentication)

### /reports&lt;int:report_id&gt;
- **HTTP request verb**: PUT, PATCH
- **Required data where applicable**: N/A
- **Expected response data**: '200 OK',  aisle width, date created, image, store id, report id
- **Authentication methods where applicable**: Admin or associated user only (JWT bearer token authentication)

### /reports/&lt;int:report_id&gt;
- **HTTP request verb**: DELETE
- **Required data where applicable**: N/A
- **Expected response data**: '200 OK', empty JSON string
- **Authentication methods where applicable**: Admin or associated user only (JWT bearer token authentication)


## An ERD for your app
![CRAMPT Entity Relationship Diagram (ERD)](/docs/ERD.png)

*CRAMPT Entity Relationship Diagram*


## Detail any third party services that your app will use
### Flask
Flask is a web application microframework for Python. It is a Web Server Gateway Interface (WSGI) framework that helps receive HTTP requests, route requests to Python functions and return HTTP responses, as well as manage errors and redirects. It easily integrates with a variety of extensions for Object Relational Mapping (e.g., SQLAlchemy), encryption (e.g., Bcrypt) and authentication (e.g., JWTManager).

### PostgreSQL
PostgreSQL is a relational database management system (RDBMS) that supports relational (SQL) and non-relational (JSON) queries. It is commonly used as a back-end database for web applications due to its support for a wide range of programming languages and its ability to manage complex database relations and queries.

### SQLAlchemy
SQLAlchemy is an Object Relational Mapper (ORM) for Python.  python library that serves as an object relational mapper (ORM). It enables the replacement of complex raw SQL queries with simpler and more straightforward python code. By associating database tables with python classes, SQL Alchemy facilitates the execution of queries in a convenient and efficient manner.

### psycopg2
psycopg2 is a python adapter that facilitates the connection and manipulation of PostgreSQL databases through python programs. It maps Python's object orienting programming (OOP) to SQL relational databases, delegating SQL queries to powerful and adaptable OOP capabilities. 

### marshmallow
marshmallow is a Python library for converting complex data types such as JSON into Python data types such as dictionaries and vice versa through schemas. It also offers powerful validation classes to sanitise inputs and raise errors.

### bcrypt
Bcrypt is a password-hashing function that uses a random 16-byte salt to securely encrypt data. It is commonly used to avoid sensitive data, such as passwords, being stored in databases as plain text. 

### Flask-JWT-Extended
Flask-JWT-Extended is a Python library that supports the use of JSON Web Tokens (JWT) to authenticate access to protected routes. It helps create JWTs, set protected routes and get the identity of a JWT, as well as additional functions, such as setting the expiry of JWTs.


## Describe your projects models in terms of the relationships they have with each other
### User
The `users` SQLAlchemy model consists of the following class attributes:

- <u>`id`: integer __[primary key]__</u>
- `email`: string (unique and mandatory)
- `password`: string (mandatory)
- `is_admin`: boolean (False by default)

It has a back-populating, one-to-many relationship with the `reports` model, . This relationship cascades on delete, meaning if a user is deleted, all of their associated reports are deleted too.

### Store
The `stores` SQLAlchemy model consists of the following class attributes:

- <u>`id`: integer __[primary key]__</u>
- `name`: string (unique and mandatory)
- `address`: string (mandatory)
- `suburb`: string (mandatory)
- `state`: string (mandatory)
- `email`: string
- `phone_number`: string
- `aisle_width`: integer

It has a back-populating, one-to-many relationship with the `reports` model, . This relationship cascades on delete, meaning if a user is deleted, all of their associated reports are deleted too.

### Reports
The `reports` SQLAlchemy model consists of the following class attributes:

- <u>`id`: integer __[primary key]__</u>
- `aisle_width`: integer (mandatory)
- `image`: string
- `date_created`: date (defaults to today's date)
- `user_id`: (mandatory) __[foreign key]__
- `store_id`: (mandatory) __[foreign key]__

It has a back-populating, many-to-one relationship with the `users` and `stores` models, through the use of foreign keys. This allows users to have many reports and stores to have many reports, but each report restricted to one and only one user and one and only one store.


## Discuss the database relations to be implemented in your application
The CRAMPT database comprises three tables: `users`, `reports` and `stores`.

The `users` table consists of the following attributes:
- `id`: This is the primary key, which acts as a unique identifier for users in the database.
- `email`: This is a string representing the user's email address, which allows for optional communications with users. While `id` is the unique identifier within the database, `email` is a unique identifier on the client side for the purposes of registering and logging in as a user. However, `email` is not used as the primary key in the database, as this is not secure and would contravene Australian privacy laws.
- `password`: This is a string representing the user's password, which enables the database to authenticate and authorise users. It is not unique, as users may have the same passwords. For security purposes, the password is encrypted by bcrypt before it is stored on the database.
- `is_admin`: This is a Boolean value indicating whether the user is an admin or not, which allows for authenticating users according to permissions. It is set to False by default.

The `stores` table consists of the following attributes:
- `id`: This is the primary key, which acts as a unique identifier for stores in the database.
- `name`: This is a string representing a store's unique name. Most Chemist Warehouse store names begin with 'Chemist Warehouse' and end with the name of the suburb; however, this is not always the case – e.g., 'Airport West Pharmacy', 'Discount Chemist Langwarrin', 'Australian Open Pop-Up' – so further database normalisation for `name` is not feasible.
- `address`: This is a string representing a store's street address. It is the atomic value for addresses, despite containing different datatypes (e.g., integers for street numbers and strings for street names). For example, some street numbers are not purely integers (e.g., 'Shop SP032 Cranbourne Park', 'G089 Bayside Shopping Centre', '36 to 38 Eaton Mall', etc.).
- `suburb`: This is a string representing a store's suburb.
- `email`: This is a string representing a store's email address.
- `phone_number`: This is a string representing a store's phone number. Even though it contains only digits, it is not considered as an integer, as it may contain leading zeroes, which have no mathematical value.
- `aisle_width`: This is an integer representing a store's aisle width, in centimetres.

The `reports` table consists of the following attributes:
- `id`: This is the primary key, which acts as a unique identifier for stores in the database.
- `aisle_width`: This is an integer representing a report of a store's aisle width, in centimetres.
- `image`: This is a string representing a URL providing evidence for a report.
- `date_created`: This is a date representing the date of the report's creation. It defaults to the date a report is created.
- `user_id`: This is an integer foreign key that maps to the `id` attribute in the `users` table, linking reports with a unique user tuple. This manages a many-to-one relationship between `reports` and `users`, with users able to have many reports, but each report connecting to one and only one user.
 - `store_id`: This is an integer foreign key that maps to the `id` attribute in the `stores` table, linking reports with a unique store tuple. This manages a many-to-one relationship between `reports` and `stores`, with stores able to have many reports, but each report connecting to one and only one store.

## Describe the way tasks are allocated and tracked in your project
Tasks were allocated and tracked using the project management tool Linear. 

At the outset, the following main parent and child tasks were identified:

- Create database
    - Users table
    - Reports table
    - Stores table
- Set up server
    - Create .flaskenv and .flaskenv.example
- Establish models
    - Users model
    - Reports model
    - Stores model
- Design blueprints
    - Users blueprint
    - Reports blueprint
    - Stores blueprint
    - Command line prompts blueprint
- Add authorisation
- Implement error handling and input validation
- Refactor code
- Generate requirements.txt

A stretch goal of hooking into Chemist Warehouse's store locator API was also noted.

Using a Kanban board view, tasks were split under the headings 'Backlog', 'To Do', 'In Progress', 'Done' and 'Cancelled'. They were assigned varying levels of priority (low, medium, high), type labels (feature, improvement) and expected completion dates, and blocking/blocked relationships were mapped. New tasks that emerged during the course of development, e.g., bugs, were promptly added to the Kanban board and classified in the same way.

With task expected completion dates mapping the entire development period, I was able to treat each day as a micro scrum sprint. Each morning, I conducted a solo stand up to reflect on what I achieved the day before, what I needed to complete that day and what hurdles I was facing.

Initially, all tasks were placed in the 'Backlog' queue. On a task's expected completion date, they were moved to the 'To Do' queue. When deciding on what task to begin, I applied the following criteria in order:

- Highest priority (low, medium, high)
- Number of blocking relationships (if any)
- Smallest expected time to complete

Tasks were moved to the 'In Progress' queue when I began work on them, then moved to 'Done' when completed. In line with my micro scrum sprint approach, I endeavoured to have no tasks in the 'In Progress' queue at the end of any given day. When this was unavoidable, I took the opportunity to further reflect on and refine my timelines and general approach during a sprint review at the next morning's stand up.

The following screenshots provide an indication of how development was organised and managed:

![Kanban, 6 December 2023](/docs/Kanban_20231206.png)
*Kanban, 6 December 2023*

![Kanban, 7 December 2023](/docs/Kanban_20231207.png)
*Kanban, 7 December 2023*

![Kanban, 8 December 2023](/docs/Kanban_20231208.png)
*Kanban, 8 December 2023*

![Kanban, 12 December 2023](/docs/Kanban_20231212.png)
*Kanban, 12 December 2023*

![Kanban, 13 December 2023](/docs/Kanban_20231213.png)
*Kanban, 13 December 2023*

Detailed information about the daily progress of each task has been captured in the following `md` files:

[6 December 2023](/docs/Kanban_20231206.md)

[7 December 2023](/docs/Kanban_20231207.md)

[8 December 2023](/docs/Kanban_20231208.md)

[12 December 2023](/docs/Kanban_20231212.md)

[13 December 2023](/docs/Kanban_20231212.md)