# BabyTracker 🍼

BabyTracker is a sophisticated Flask application designed to simplify and enhance the tracking of baby activities,
including feeding times, sleep schedules, and diaper changes. Utilizing a user-friendly interface and backed by a robust
database, BabyTracker aims to provide parents and caregivers with a seamless experience to monitor and analyze their
baby's daily routines.

## Features

- **Activities Tracker:** Log feeding, sleeping, diaper changes, and medicine as quick as clicking a button.
- **Growth Tracking:** Input measurements of the baby's length to track growth over time.
- **Percentile Visualization:** View entered data through charts and graphs, making it easier to spot trends.

## Usage

After launching BabyTracker, you will be asked to create an account or log in if you already have one.
Once logged in, you can start tracking your baby's activities by clicking on the relevant buttons to submit new entries
for feedings, sleep, diaper changes, and medicine tracking.
On the Percentile page, you can enter your baby's measurements to track their growth over time.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing
purposes.

### Prerequisites

| Requirement | Version |
|-------------|---------|
| Python      | 3.8+    |
| pip         | Latest  |

### Installation

1. Clone the repository to your local machine:
   ```bash
   git clone https://github.com/danielfriw/BabyTracker.git
   ```
2. Navigate to the cloned repository:
   ```bash
   cd BabyTracker
   ```
3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up the environment variables:
   ```bash
   export FLASK_APP=babytracker
   export FLASK_ENV=development
   ```
5. Run the application:
   ```bash
   flask run
   ```
   The application will be accessible at `http://127.0.0.1:5000/`. Ensure that you have set the `FLASK_APP`
   and `FLASK_ENV` environment variables as described in the installation instructions.

Remember to follow the Flask and Python best practices for managing your environment variables and dependencies to
maintain a secure and efficient development environment.

### Testing

This project uses pytest for unit testing to ensure the application functions as expected. Our tests primarily cover
unit tests at this stage. You can find all tests in the `tests` folder.

To run the tests, first, ensure you have pytest installed. If not, you can install it using pip:

```bash
pip install pytest
```

Then, execute the following command from the project root directory:

```bash
pytest
```

### Technical Setup

The application's entry point is the `app.py` file, where the Flask app instance is created and configured.
The `extensions.py` file initializes the database (DB) and login manager, which are then coupled to the Flask app as
seen in the `app.py`. This approach allows for a modular and organized code structure, facilitating easier maintenance
and scalability.

### Application Structure

- **Blueprints:** The application logic is divided into blueprints, each responsible for a different aspect of the
  application (authentication, baby tracking, events, etc.). These blueprints are located under the `main/blueprints`
  directory.

- **Database and Migrations:** SQLite is used as the database, with Flask-Migrate managing database migrations. The
  database is initialized and migrations are set up in `extensions.py`.

- **Templates:** HTML templates are stored in the `templates` directory in each blueprint. The only exclusion is
  the `base.html`, which serves as the layout template for the application. The `base.html` file contains the navigation
  bar and header buttons that are common across the application and is located in a `templates` file in the main
  directory.

- **Static Files:** CSS and JavaScript files are stored in the `static` directory in each blueprint, allowing for custom
  styling and interactivity on the web pages.

- **Utility Functions:** The `main/utils` directory contains utility functions that are used across different parts of
  the application. This includes context processors and helper functions that support the application's functionality.

- **Configuration:** The Flask app is configured in `app.py`, including database URI, secret key, and other application
  settings. This setup supports both development and testing configurations.

By organizing the project in this manner, we ensure that each component is easily accessible and can be independently
developed and tested.

## Database API

<details>
<summary><b>Accessing the API</b></summary>
<p>

The BabyTracker API provides a simple interface to interact with the application's database, allowing users to retrieve,
add, or delete information programmatically. Here's a quick guide on how to use the API:

### API Endpoints

- **GET Request:** To fetch data from the database, use the GET method. For example, to retrieve information about a
  baby with a specific ID, you can use:
  ```python
  requests.get("http://127.0.0.1:5000/api/baby/<baby_id>/<baby_name>")
  ```
- **POST Request:** To add new data to the database, use the POST method with the necessary data and headers. For
  instance, to add a new baby's information:
  ```python
  requests.post("http://127.0.0.1:5000/api/baby/<baby_id>/<baby_name>",
                     data={"gender": "f", "dob": "YYYY-MM-DD"},
                     headers={"Content-Type": "application/json"})
  ```
- **DELETE Request:** To remove data from the database, use the DELETE method. For example, to delete a baby's
  information:
  ```python
  requests.delete("http://127.0.0.1:5000/api/baby/<baby_id>/<baby_name>")
  ```

</p>
</details>

## Contributing 👨‍💻

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any
contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Contact 📫

Daniel Friedman - danielfri@wix.com

Project Link: [https://github.com/danielfriw/BabyTracker](https://github.com/danielfriw/BabyTracker)

## Acknowledgments

- Flask for the awesome micro-framework that makes web app development a breeze.
- Chart.js for the beautiful data visualization tools.
- SQLite for providing a simple and reliable database solution.
- All contributors who help to make BabyTracker better.
