
# SmsHub API Wrapper

This library provides a simple and intuitive Python wrapper around the SmsHub API, allowing for both synchronous and asynchronous interaction with the service. With this wrapper, you can easily integrate SmsHub functionality into your Python applications.

## Features

- Synchronous and asynchronous API calls.
- Comprehensive error handling with custom exceptions.
- Response parsing utilities.
- Support RU/EN languages based on system settings.

## Installation

To install SmsHub API Wrapper, simply use pip:

```bash
pip install pysmshub
```

## Quick Start

Here's a quick example of how you can use the SmsHub API Wrapper:

Synchronous usage

```python
import time
from pysmshub import SyncSmsHubApi
from pysmshub.utils import Status

# Initialize instance with API_KEY. HTTP proxy support available.
hub_api_sync = SyncSmsHubApi(api_key="your_api_key_here", proxy="http://proxyhost:proxyport")

# Get_balance example
balance = hub_api_sync.get_balance()
print(f"Current balance: {balance}")

# Get_number example
num_id, phone = hub_api_sync.get_number(service="ya", max_price=2)

# Get_status example
for _ in range(10):
    status, code = hub_api_sync.get_status("your_num_id")
    if status == Status.SUCCESS:
        print(code)
        break
    time.sleep(1)

# Set_status example
hub_api_sync.set_status("your_num_id", Status.CANCEL)
```
Asynchronous usage

```python
import asyncio
from pysmshub import AsyncSmsHubApi
from pysmshub.utils import Status


async def async_example():
    # Initialize instance with API_KEY
    hub_api_async = AsyncSmsHubApi(api_key="your_api_key_here")

    # Get_balance example
    balance = await hub_api_async.get_balance()
    print(f"Current balance: {balance}")

    # Get_number example
    num_id, phone = await hub_api_async.get_number(service="ya", max_price=2)

    # Get_status example
    for _ in range(10):
        status, code = await hub_api_async.get_status("your_num_id")
        if status == Status.SUCCESS:
            print(code)
            break
        await asyncio.sleep(1)

    # Set_status example
    await hub_api_async.set_status("your_num_id", Status.CANCEL)


# Run the async example
asyncio.run(async_example())
```

Error handling

```python
from pysmshub import SyncSmsHubApi

hub_api_sync = SyncSmsHubApi(api_key="your_api_key_here")
try:
    num_id, phone = hub_api_sync.get_number(service="ya", max_price=2)
except SmsHubApiException as e:
    print(e)
```
Proxy support

```python
from pysmshub import SyncSmsHubApi, AsyncSyncSmsHubApi

SyncSmsHubApi(api_key="your_api_key_here", proxy="http://proxyhost:proxyport")
AsyncSyncSmsHubApi(api_key="your_api_key_here", proxy="http://proxyhost:proxyport")
```

## Documentation

For detailed information about all the functionality available in this wrapper, please refer to the [official SmsHub API documentation](https://smshub.org/ru/info).

## Contributing

Contributions are welcome! If you have an improvement or a bug fix, feel free to fork this repository, make your changes, and submit a pull request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

If you need help or have any questions, please open an issue in the [GitHub issue tracker](https://github.com/kuudori/smshubapi/issues).

## Disclaimer

This library is not affiliated with SmsHub and is developed as an independent project.
