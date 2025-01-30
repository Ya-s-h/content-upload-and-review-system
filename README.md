# Content Upload and Review System

## Overview
The **Content Upload and Review System** is a web application designed to handle content uploads, organization, and reviews. It provides APIs to manage content-related operations efficiently.

## Features
- Upload and manage content (movies, documents, etc.)
- API endpoints for handling content operations
- Modular structure with routes, models, and utilities

## Project Structure
```
content-upload-and-review-system/
│── app/
│   ├── models/          # Data models (e.g., movies)
│   ├── routes/          # API routes (movies, uploads)
│   ├── app.py           # Main application file
│── .gitignore
│── README.md
```

## Installation
### Prerequisites
- Python 3.10+
- Virtual environment (optional but recommended)

### Steps
1. Clone the repository:
   ```sh
   git clone https://github.com/Ya-s-h/content-upload-and-review-system.git
   cd content-upload-and-review-system
   ```
2. Create and activate a virtual environment (optional but recommended):
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

## Usage
### Running the Application
```sh
python app/app.py
```

### API Endpoints
The application exposes several endpoints, primarily for managing movie content and uploads. Here are some examples:
- `POST /upload` - Upload content
- `GET /movies` - Retrieve movie listings

## Contributing
Contributions are welcome! Feel free to submit a pull request or open an issue.

## License
This project is licensed under the MIT License.

## Testing
Postman Collection is added for testing purposes