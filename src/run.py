import uvicorn
import sys
import asyncio

if __name__ == '__main__':
    if sys.platform.startswith('win'):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    uvicorn.run(app='api.main:app', host='127.0.0.1', port=8000, reload=True)