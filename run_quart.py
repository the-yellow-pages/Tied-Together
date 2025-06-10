#!/usr/bin/env python3
"""
Startup script for Quart application using Hypercorn ASGI server
"""
import os
import asyncio
from hypercorn.config import Config
from hypercorn.asyncio import serve
from app import app

def create_hypercorn_config():
    """Create Hypercorn configuration"""
    config = Config()
    config.bind = [f"0.0.0.0:{int(os.environ.get('PORT', 5000))}"]
    config.loglevel = "info"
    config.access_log_format = "%(h)s %(r)s %(s)s %(b)s %(D)s"
    config.access_log = "-"  # Log to stdout
    config.error_log = "-"   # Log to stderr
    
    # Development settings
    if os.environ.get('ENVIRONMENT') == 'development':
        config.debug = True
        config.use_reloader = True
    
    return config

async def main():
    """Main async function to run the server"""
    config = create_hypercorn_config()
    await serve(app, config)

if __name__ == "__main__":
    asyncio.run(main())
