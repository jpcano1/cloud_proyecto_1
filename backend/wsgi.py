from src import app
import os

if __name__ == "__main__":
    app.run(
        host=os.getenv("HOST", "0.0.0.0"),
    )