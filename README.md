# Digital Pulse Job Task

## User Story
You have a new project in which you'll develop a Communities Management application using Python, Django, and DRF. Your focus is to create an API that will meet all the requirements needed to manage communities, users, and roles with PostMan collection as documentation and show your strength in your stack.

## Requirements
- Develop a Django API for this project.
- Use Just Django-related libraries.
- Express Your knowledge of Django features.
- At least the User model and Community model where there have at least these attributes (The user can enter multiple communities where he has a position in this community)

    **User Model**
    1. name 
    2. username
    3. password
    4. email
    5. location (Latitude and longitude)
    6. phone number


    **Community Model**
    1. name 
    2. address  (Latitude and longitude)
    3. members ( Many to Many with User with position field)


- Multiple endpoints where you can:

    - sign up
    - sign in 
    - Do CRUD operation on the user model.
    - Do CRUD oprations on comunity model.
    - Add user to a community.
    - Get community users.
    - Get nearby communities without using any external API, asume that the community is near the user if it's in a circle from the user of a radius of 2km.

## Submission

**Postman Collection Documentation:** https://documenter.getpostman.com/view/29210765/2s9Y5VTP5Z