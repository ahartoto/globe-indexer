# Filename: run.py

# Globe Indexer
from globe_indexer import app


# Interface functions
def main():
    """
    Main function for the application
    """
    app.run(port=8080)


# Entry point
if __name__ == '__main__':
    main()
