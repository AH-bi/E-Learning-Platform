
# QCM E-learning Platform

This project is an **E-learning platform** designed to provide question-based learning (QCM) where topics can be chosen by an admin or teacher. It offers a competitive game mode where users can play against the computer or remotely with friends. The system includes a leaderboard and review features to check answers after completing the questions.

## Features

- **User Authentication**: Register, Login, Logout functionalities.
- **Question Management**: Add, edit, and delete questions based on topics.
- **Competitive Game Mode**: Play against the computer or remotely with friends.
- **Leaderboard**: Track performance and scores of players.
- **Answer Review**: After completing questions, users can review their answers to see if they are correct.
- **Admin Dashboard**: Customizable admin dashboard to manage users, topics, questions, and track any activity on the platform.
- **SQLite Database**: Default SQLite database for development purposes.



## Installation

### 1. Clone the repository:
```bash
git clone https://github.com/AH-bi/e-learning.git
cd qcm
```

### 2. Set up the virtual environment based on your operating system:

For **Linux/macOS**:
```bash
python3 -m venv myenv
source myenv/bin/activate
```

For **Windows**:
```bash
python -m venv myenv
myenv\Scripts\activate
```

### 3. Install dependencies:
```bash
pip install -r requirements.txt
```

### 4. Apply migrations:
```bash
python manage.py migrate
```

### 5. Run the development server:
```bash
python manage.py runserver
```

### 6. Create a superuser (optional, for accessing the admin dashboard):
```bash
python manage.py createsuperuser
```

## Usage

- Access the admin panel at `http://127.0.0.1:8000/admin/` to manage users, topics, and questions.
- Interact with the application through the user interface and participate in quizzes or the competitive game mode.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
