# Trees Everywhere

Trees Everywhere is a Django-based project aimed at promoting the plantation and management of trees. The project allows users to register, create profiles, and track the trees they have planted. This project was made for the [**YouShop**](https://www.linkedin.com/company/youshop-brasil/) selective process.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)
- [Models](#models)
- [Contributing](#contributing)
- [License](#license)

## Installation

### Prerequisites

- Python 3.10 or higher
- Django 4.2 or higher
- Poetry for dependency management

### Setup

1. Clone the repository:

   ```bash
   git clone git@github.com:leonardo-caixeta/Trees-Everywhere.git
   cd Trees-Everywhere
   ```

2. Install dependencies using Poetry:

   ```bash
   poetry install --no-root
   ```

3. Setup the Poetry virtual environment:

   ```bash
   poetry shell
   ```

4. Apply database migrations:

   ```bash
   python manage.py migrate
   ```

5. Create a superuser:

   ```bash
   python manage.py createsuperuser
   ```

6. Run the development server:

   ```bash
   python manage.py runserver
   ```

## Usage

1. Access the development server at [`http://127.0.0.1:8000`](http://127.0.0.1:8000) [`(http://localhost:8000)`](http://127.0.0.1:8000).
2. Register a new user account or log in with the superuser account.
3. Create and manage tree plantations through the provided interfaces.

## Features

- User registration and authentication
- User profile management
- Tree plantation tracking
- Admin interface for managing users and tree data

## Models

Here is the content organized into a table:

| Model         | Description                                         |
|---------------|-----------------------------------------------------|
| User          | Represents a registered user.                       |
| Profile       | Extended user profile with additional information.  |
| Account       | Financial account related to user activities.       |
| Tree          | Information about different types of trees available for planting. |
| PlantedTree   | Tracks the trees planted by users.                  |

## Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -m 'feat: your feat message'`).
4. Push to the branch (`git push origin feature-branch`).
5. Open a pull request.

## API Endpoints

### Authentication
- `POST /login/`: User login

### User Trees
- `POST /tree/add/`: Add a new tree to the system
- `POST /tree/plant/`: Plant a new tree
- `GET /user/trees/`: List trees associated with the user
- `GET /tree/<int:pk>/`: Retrieve details of a specific tree
- `GET /account/trees/`: List trees associated with the user's account
- `GET /api/user/trees/`: API endpoint for listing trees planted by the user
