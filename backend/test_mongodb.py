from pymongo import MongoClient
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_mongodb_connection():
    try:
        # MongoDB connection string
        uri = "mongodb+srv://alireza:ali1378reza1742@cluster0.ug6m1cu.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
        
        # Create a new client and connect to the server
        client = MongoClient(
            uri,
            serverSelectionTimeoutMS=5000,
            tls=True,
            tlsAllowInvalidCertificates=True  # Allow invalid certificates for testing
        )
        
        # Send a ping to confirm a successful connection
        client.admin.command('ping')
        logger.info("Successfully connected to MongoDB!")
        
        # List all databases
        databases = client.list_database_names()
        logger.info(f"Available databases: {databases}")
        
        # Check if negar_studio database exists
        if 'negar_studio' in databases:
            logger.info("negar_studio database exists")
            # List collections in negar_studio
            db = client['negar_studio']
            collections = db.list_collection_names()
            logger.info(f"Collections in negar_studio: {collections}")
        else:
            logger.info("negar_studio database does not exist")
        
        # Close the connection
        client.close()
        
    except Exception as e:
        logger.error(f"Error connecting to MongoDB: {str(e)}")

if __name__ == "__main__":
    test_mongodb_connection() 