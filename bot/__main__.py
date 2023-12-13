if __name__ == "__main__":
    import asyncio
    import logging
    import sys

    if sys.version_info < (3, 10):
        sys.exit("Please use Python 3.10+")

    from bot.main import main

    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Bot stopped")