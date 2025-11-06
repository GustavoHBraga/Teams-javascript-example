"""
Database connection and models using Motor (async MongoDB)
"""
from motor.motor_asyncio import AsyncIOMotorClient
from shared.config import settings

# Cliente MongoDB
client: AsyncIOMotorClient = None
database = None


async def connect_db():
    """Conecta ao MongoDB"""
    global client, database
    
    client = AsyncIOMotorClient(settings.mongodb_url)
    database = client[settings.mongodb_db_name]
    
    print(f"✅ Conectado ao MongoDB: {settings.mongodb_db_name}")


async def close_db():
    """Fecha conexão com MongoDB"""
    global client
    
    if client:
        client.close()
        print("❌ Conexão MongoDB fechada")


def get_database():
    """Retorna instância do database"""
    return database
