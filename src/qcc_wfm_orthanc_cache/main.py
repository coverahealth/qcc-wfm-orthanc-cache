import asyncio

from covera_ddtrace import inject_ddtrace


@inject_ddtrace
async def main():
    print("Hello from Covera Template")


if __name__ == "__main__":
    asyncio.run(main())
