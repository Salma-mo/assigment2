Steps to Set Up the Project:

1. Open Visual Studio Code and open the project folder.
2. Open the terminal in VS Code (Ctrl + ~).
3. Create a virtual environment using the command:
   python -m venv venv
4. Activate the virtual environment:
   For Windows (PowerShell):
   venv\Scripts\activate

   For Windows (CMD):
   venv\Scripts\activate.bat

5. Install required dependencies:
   pip install flask flask-sqlalchemy flask-jwt-extended bcrypt python-dotenv

6. Create a `.env` file in the project directory and add the following:
   DATABASE_URL=sqlite:///data.db
   JWT_SECRET=supersecretkey

7. Run the application:
   python app.py

8. The server will start running at:
   http://127.0.0.1:5000

