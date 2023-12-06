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
- **Required data where applicable**: 
- **Expected response data**: List of all users.
- **Authentication methods where applicable**: Admin only

### /users
- **HTTP request verb**: POST
- **Required data where applicable**: 
- **Expected response data**: Create a new user
- **Authentication methods where applicable**: Admin only

### /users/<int:user_id>
- **HTTP request verb**: PATCH
- **Required data where applicable**: 
- **Expected response data**: Update a user, e.g., provide admin access
- **Authentication methods where applicable**: Admin only

### /users/<int:user_id>
- **HTTP request verb**: DELETE
- **Required data where applicable**: 
- **Expected response data**: Delete a user
- **Authentication methods where applicable**: Admin only

### /auth/register
- **HTTP request verb**: POST
- **Required data where applicable**: 
- **Expected response data**: Register as a user
- **Authentication methods where applicable**: Admin only

### /auth/login
- **HTTP request verb**: POST
- **Required data where applicable**: 
- **Expected response data**: Login as a user
- **Authentication methods where applicable**: Admin only

### /reports
- **HTTP request verb**: GET
- **Required data where applicable**: 
- **Expected response data**: List of all reports.
- **Authentication methods where applicable**: Admin only

### /stores
- **HTTP request verb**: GET
- **Required data where applicable**: 
- **Expected response data**: List of all stores.
- **Authentication methods where applicable**:

### TO DO: more routes


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


## Discuss the database relations to be implemented in your application
The CRAMPT database comprises three tables: `users`, `reports` and `stores`.


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

Detailed information about the daily progress of each task has been captured in the following `md` files:

[6 December 2023](/docs/Kanban_20231206.md)

