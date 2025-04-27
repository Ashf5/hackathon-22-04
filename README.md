# 🎬 Movie Recommendation Console App

A Python console application where users input movies they enjoy. After entering movies, the program provides personalized movie recommendations with descriptions — based on their taste!

---

## ✨ Features

- Accepts and stores user movie preferences in a PostgreSQL database
- Smart movie suggestions based on user input
- Fetches movie details using the TMDB API
- Smart recommendation generation using OpenAI
- Runs completely in the console (no web interface)

---

## 🛠 Installation

1. **Clone the repository**
    ```bash
    git clone https://github.com/Ashf5/hackathon-22-04.git
    cd hackathon-22-04
    ```

2. **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3. **Set up your database**
    - Create a PostgreSQL database.
    - Create the necessary tables using the schema provided in `notes.txt`.
    - Update the database credentials in:
      - `postgres_helpers.py`
      - `password_tools.py`

4. **Configure API keys**
    - Obtain an **OpenAI API key** and a **TMDB API key**.
    - Update `password_tools.py` with your API keys and paths to your password storage files.

---

## 🚀 Usage

Run the app directly from your console:

```bash
python main.py
