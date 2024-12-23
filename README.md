# Redis Priority Queue Implementation

A Python implementation of a priority queue using Redis as the backend storage. This implementation demonstrates how to handle tasks with different priority levels while ensuring each task is processed exactly once, even with multiple consumers.

The project includes both synchronous (thread-based) and asynchronous (asyncio-based) implementations.

## Features

- Priority-based task processing (1=high, 2=medium, 3=low)
- Multiple consumers can process tasks concurrently
- No duplicate processing of tasks
- Real-time task distribution
- Timestamps for task creation and processing
- Graceful shutdown handling
- Both synchronous and asynchronous implementations

## Prerequisites

- Python 3.6+
- Redis server running on localhost:6379
- Python packages:
  ```
  redis>=4.5.0    # Includes both sync and async implementations
  ```

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/redis-priority-queue.git
   cd redis-priority-queue
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Ensure Redis server is running:
   ```bash
   # On macOS with Homebrew
   brew services start redis
   
   # On Ubuntu/Debian
   sudo service redis-server start
   ```

## Project Structure

```
redis-priority-queue/
├── async/                  # Asyncio-based implementation
│   ├── redis_pq.py        # Core async implementation using redis.asyncio
│   ├── producer.py        # Async producer
│   ├── consumer_1.py      # First async consumer
│   └── consumer_2.py      # Second async consumer
├── sync/                  # Thread-based implementation
│   ├── redis_pq.py        # Core sync implementation using redis
│   ├── producer.py        # Threaded producer
│   ├── consumer_1.py      # First threaded consumer
│   └── consumer_2.py      # Second threaded consumer
├── requirements.txt       # Project dependencies
└── README.md             # This file
```

## Running the Demo

You can choose to run either the synchronous or asynchronous version:

### Synchronous Version (Thread-based)

1. Start the producer in one terminal:
   ```bash
   python sync/producer.py
   ```

2. Start the first consumer in another terminal:
   ```bash
   python sync/consumer_1.py
   ```

3. Start the second consumer in a third terminal:
   ```bash
   python sync/consumer_2.py
   ```

### Asynchronous Version (Asyncio-based)

1. Start the producer in one terminal:
   ```bash
   python async/producer.py
   ```

2. Start the first consumer in another terminal:
   ```bash
   python async/consumer_1.py
   ```

3. Start the second consumer in a third terminal:
   ```bash
   python async/consumer_2.py
   ```

You'll see the following in both versions:
- Producer generating tasks with random priorities
- Tasks being distributed between consumers
- Each task processed exactly once
- Higher priority tasks processed before lower priority ones

To stop any component, press Ctrl+C in its terminal.

## Implementation Details

### Synchronous Version
- Uses the `redis` Python package
- Thread-based workers
- Blocking Redis operations
- Simple to understand and debug

### Asynchronous Version
- Uses `redis.asyncio` from the Redis package
- Asyncio-based workers
- Non-blocking Redis operations
- Better performance for I/O-bound operations
- More scalable for large numbers of tasks

Both versions use Redis sorted sets (ZSET) for:
- `ZADD` to add tasks with priority as score
- `ZRANGE` to get the highest priority task
- `ZREM` to remove processed tasks
- Atomic operations to ensure no duplicate processing

## Example Output

```
[Producer] Generated task:
  - Task ID: 1234
  - Type: email
  - Priority: high
  - Created at: 14:30:14

[Consumer 1] Got task:
  - Task ID: 1234
  - Created at: 14:30:14
  - Type: email
  - Priority: high
  - Payload: High priority email task
```

## Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.

## License

This project is licensed under the MIT License - see the LICENSE file for details.