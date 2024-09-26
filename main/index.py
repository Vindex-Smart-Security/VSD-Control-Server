import asyncio
from utils.Init import StartUp, handle_exit

async def main():
    shutdown_event = asyncio.Event() 
    await asyncio.gather(
        StartUp(shutdown_event),  
        handle_exit(shutdown_event) 
    )

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except SystemExit:
        pass 