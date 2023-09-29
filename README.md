# Pet Adopt API 🐾

## Table of Contents

- [Introduction](#introduction)
- [Technologies](#technologies)
- [URL Routing and Nested Routes](#url-routing-and-nested-routes)
- [Database](#database)
- [Security](#security)
- [Deployment](#deployment)
- [Further Possibilities](#further-possibilities)
- [What I Learned](#what-i-learned)
- [Documentation](#documentation)

## Introduction

This project is a backend API developed using Django and the Django REST Framework. It's designed to facilitate pet adoption, providing endpoints for managing users, pets, and their respective attributes such as tags and shelters.

## Technologies

- **Backend**: Python, Django, Django REST framework
- **Database**: PostgreSQL


## URL Routing and Nested Routes

One of the more complex parts of this API is the routing configuration. Not only does it handle the standard CRUD operations for each model, but it also uses nested routes for more context-specific operations.

### Main Routes

- **Pets**: Endpoint for managing and retrieving pets.
- **Shelters**: Endpoint for managing and retrieving shelters.
- **Users**: Endpoint for managing and retrieving users.
- **Tags**: Endpoint for managing and retrieving tags.
- **Comments**: Endpoint for managing and retrieving comments.

### Nested Routes

#### For Users
- **Comments**: Nested under users, this endpoint manages comments associated with a particular user.
- **Likes**: Nested under users, this endpoint manages likes made by a particular user.
- **Pets**: Nested under users, this endpoint manages pets associated with a particular user.

#### For Pets
- **Comments**: Nested under pets, this endpoint manages comments associated with a particular pet.
- **Likes**: Nested under pets, this endpoint manages likes for a particular pet.
- **Tags**: Nested under pets, this endpoint manages tags associated with a particular pet.

#### For Shelters
- **Pets**: Nested under shelters, this endpoint manages pets that are part of a particular shelter.

### Authentication Routes

- **Register**: Endpoint for user registration.
- **Login**: Endpoint for user login.

### Documentation Routes

- **Docs**: Provides autogenerated documentation for the API.
- **Schema**: Provides the schema view for the API, detailing how the data models are constructed.

The use of `rest_framework_nested` routers enables the nesting of routes, providing a more logical and intuitive way to access related resources. This contributes to making the API more RESTful and easy to understand.

## Database 

The database consists of several models, closely mirroring the real-world entities involved in pet adoption:

- **UserProfile**: Stores additional user information including image and location.
- **Shelter**: Contains shelter details such as name, location, and description.
- **Pet**: Holds comprehensive information about each pet including age, type, and associated tags.
- **Comment**: Captures user comments on pets.
- **Like**: Records likes on pets by users.
- **Tag**: Stores tags that describe pet personality traits.

## Security

- Passwords are securely hashed before storage.
- Different permission levels are implemented using Django's permission classes.

## Deployment

The API is deployed on Heroku, ensuring high availability and robust performance. You can access it [here](https://petadopt-431a50d84aab.herokuapp.com/).

## Further Possibilities

- Implementing more advanced filtering options.
- Adding rate limiting to the API.
- Adding a caching layer for better performance.
- Enhanced User Profiles
- Real-Time Notifications
- Geo-Location Features

## What I Learned


- **Understanding of DRF** Gained a comprehensive understanding of Django REST Framework, including serializers, viewsets, and routers.
- **Query Optimization**: Learned how to optimize queries in Django, reducing the overhead on the database.


## Documentation

The API is thoroughly documented and can be accessed through the following:

1. [Django Rest Framework Documentation](https://petadopt-431a50d84aab.herokuapp.com/api/docs/)
2. [Django Admin](https://petadopt-431a50d84aab.herokuapp.com/admin/)
3. [Postman Documentation](https://documenter.getpostman.com/view/29119401/2s9YJXa5hr)

Each endpoint is meticulously documented, providing details on HTTP methods, query parameters, required fields for POST requests, and much more.
