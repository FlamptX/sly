import motor.motor_asyncio

class MongoDB(motor.motor_asyncio.AsyncIOMotorClient):
    '''
    Represents the main motor connection pool to the MongoDB cluster.
    
    .. This class also contains helpers to interact with databases and collections.
    '''
    def __init__(self, uri):
        self.uri     = uri
        super().__init__(self.uri)
    

    # <-- Helpers -->
    
    # These are only functions that are used frequently across the code.

    
    async def fetch_one_with_id(self, id, database, collection):
        return await self[database][collection].find_one({'_id': id})
    
    async def fetch_many_with_id(self, id, database, collection):
        return await self[database][collection].find({'_id': id})
