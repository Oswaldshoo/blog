# Simple Blog Site

This is a simple blog site built with Flask and SQLite. Users can register, log in, create blog posts, and comment on posts.

## Getting Started

To run the blog site locally, follow these instructions:

### Prerequisites

- Python (3.7 or higher)
- Pip (Python package installer)

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/oswaldshoo/blog.git
   ```

2. Navigate to the project directory:

   ```bash
   cd blog
   ```

3. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Initialize the SQLite database:

   ```bash
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade
   ```

### Usage

1. Run the Flask development server:

   ```bash
   flask run
   ```

2. Open your web browser and go to [http://localhost:5000/](http://localhost:5000/) to access the blog site.

## Features

- User Registration and Authentication
- View a List of Blog Posts
- Read Individual Blog Posts
- Add Comments to Blog Posts
- Create New Blog Posts
- Log In and Log Out

## Project Structure

- `app.py`: Main Flask application file.
- `auth.py`: User authentication routes and functions.
- `templates/`: HTML templates for rendering pages.
- `static/`: Static assets (CSS, images).


## Contributing

Contributions are welcome! Please follow the [Contribution Guidelines](CONTRIBUTING.md).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
