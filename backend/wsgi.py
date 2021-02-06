from src import app
import os

if __name__ == "__main__":
    app.run(
        host=os.getenv("HOST", "localhost"),
        port=os.getenv("PORT", 5000)
    )