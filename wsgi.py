# ASGI entry point for Quart application
from app import app

# This is the ASGI application object that can be used by ASGI servers
application = app

if __name__ == "__main__":
    # For development, run with hypercorn
    import asyncio
    from hypercorn.config import Config
    from hypercorn.asyncio import serve
    
    config = Config()
    config.bind = ["0.0.0.0:5000"]
    config.debug = True
    asyncio.run(serve(app, config))
