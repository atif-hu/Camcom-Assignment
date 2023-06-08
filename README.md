# QC Portal API documentation

This docmentation provides overview for the QC Portal API. The API is implemented using Python, Flask and MySQL DB.

In a manual QC (Quality Check) process, there is a portal from which each individual QC task is assigned. 
The portal needs to check how many QC persons are logged in and which of the logged in persons are free, as in not on a task, and automatically assign tasks. 
Once the task is finished the person will automatically get assigned the next task if any is pending. 
How would you architect this? I want to understand step by step the methodology you used to come to the final solution. 
Illustrate a basic API framework written in Python using Flask and MySql as the database.

## API Endpoints

### Login
This endpoint is used to authenticate users and obtain a JSON Web Token (JWT) for subsequent API requests.

* URL: /login<br />
* Method: POST<br />
* Request Body:
{
   username: The username of the user.
   password: The password of the user.,
}
* Response: {token: The JWT token to be used for authentication.}

### Update Availability
This endpoint is used to update the availability status of the user.

* URL: /availability
* Method: PUT
* Request Body:{user_id: The ID of the user whose availability status should be updated.,
availability: The availability status of the user (1 for available, 0 for unavailable).}
Response:
* Response: {message:A success message indicating that the availability has been updated.}

### Assign Task
This endpoint is used to automatically assign a task to an available user.

* URL: /assign_task
* Method: POST
* Request Body: {task_id: The ID of the task to be assigned.}
* Response: {message: A success message indicating that the task has been assigned.}

### Complete Task
This endpoint is used to mark a task as completed and check if there are any pending tasks for the user.

* URL: /complete_task
* Method: POST
* Request Body:{task_id: The ID of the completed task.,user_id: The ID of the user who completed}
* Response:{message: Task completed message with the status of next task pending or not}

### Database Schema
To manage and store user and task information, the database schema consists of two tables "users" and "tasks".
* users table store information about the users in the column as `user_id`, `username`, `password`, `availability`
* tasks table store information about the QC tasks in the column as `task_id`, `taskname`, `status`, `assigned_user_id`, where `assigned_user_id`
is the FOREIGN KEY referencing to user_id column in users table to indicate the user assigned to the task.
