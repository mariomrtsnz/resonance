# Resonance

A web application to connect music creators (musicians, producers, audio engineers, vocalists, songwriters, etc.) for collaboration opportunities. It functions as a specialized social network focused on finding collaborators based on skills, location preferences (remote/local), and project needs.

This project serves as a learning exercise and portfolio piece demonstrating a modern full-stack web development setup.

## Tech Stack (Planned)

- **Frontend:** React (with TypeScript), Next.js, Tailwind CSS
- **Backend:** Python, Django REST Framework (DRF), PostgreSQL
- **Containerization:** Docker, Docker Compose

## Development Setup

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/mariomrtsnz/resonance
    cd resonance
    ```

2.  **Backend Setup:**

    - Navigate to the backend directory: `cd backend`
    - Create and activate a Conda environment (or your preferred venv):

      ```bash
      # Using Conda
      conda create -n resonance-venv python=3.13 # Or your preferred Python version
      conda activate resonance-venv

      # Using standard venv
      # python -m venv venv
      # source venv/bin/activate  # On Linux/macOS
      # venv\Scripts\activate     # On Windows
      ```

    - Install dependencies:
      ```bash
      pip install -r requirements.txt
      ```
    - **Environment Variables:**

      - Copy the example environment file:
        ```bash
        # From the backend directory
        cp .env.example .env
        ```
      - Edit the `.env` file and fill in your `SECRET_KEY` and database credentials (`DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`).

    - **Database Setup:**
      - Ensure you have PostgreSQL installed and running.
      - Create a database user and database matching the details in your `.env` file.
      - Apply database migrations:
      ```bash
      python manage.py migrate
      ```

3.  **Frontend Setup:** (Instructions to be added once frontend is set up)

4.  **Running the Application:**
    - **Backend:**
      ```bash
      cd backend
      # Ensure your virtual environment is active
      python manage.py runserver
      ```
    - **Frontend:** (Instructions to be added)
