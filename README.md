# Laboratory Work 7 - API
### **Topic**: Student Attendance Management System

## Description:
A REST API developed for a Student Attendance Management System, that incorporates CRUD (Create, Read, Update, Delete) operations via HTTP Methods (GET, POST, PUT, DELETE) and role-based access (Student, Professor, Admin) using JWT Token Generation/Validation to various API Endpoints. 


## Technological Stack:
1. Language: Python,
2. Database: SQLite,
3. Framework: FastAPI,
4. Session Management: JWT.

## Functional Requirements:
### API Endpoints:
There are several endpoints related to different entities in the application, such as: Users, Attendances, Sessions, etc. that implement CRUD operations.

### API Role-based Access:
Each API Endpoint is required a specific role in order to be called, for example: students can read attendances and sessions, while Admins can perform all CRUD operations on each of the endpoints.

### CRUD Operations:
This API implemented Create, Read, Update and Delete operations on entities, giving a high level of control of the user.

### Error Handling:
Most user edge-case interactions are handled in the backend application, thus making it harder to compromise the system in work.

## Non-Functional Requirements:
### Security:
By using JWT Token that is issued by backend application and used for endpoints access, is ensured only required users can access them, enhancing overall security of the app.

### Stateless:
REST API offers a stateless approach to endpoints and APIs, thus each request that is done by users in this system is not related to any of the others, ensuring consistency and independence in responses.

### HTTP Methods:
For embedding CRUD operations, HTTP methods were used - GET for READ, POST for CREATE, PUT for UPDATE and DELETE for DELETE. Each of the request has a common format of the response, ensuring consistency and a common interface for handling responses.

### Status Codes:
Each response had individual appropriate HTTP Status Code, as well as a message and description, in order to adhere to the interface and offer as much useful information as possible.

## Link to Deployed Application:
[Student Attendance Management System API!]([https://ghenntoggy1.github.io/Clicker_Game/](https://student-management-system-api-72w4.onrender.com/docs))
