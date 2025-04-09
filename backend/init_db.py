from app import create_app, mongo

def init_db():
    app = create_app()
    with app.app_context():
        # Create a test document to initialize the database
        try:
            mongo.db.users.insert_one({'test': 'test'})
            mongo.db.users.delete_one({'test': 'test'})
            print("Database initialized successfully!")
        except Exception as e:
            print(f"Error initializing database: {str(e)}")

if __name__ == "__main__":
    init_db() 