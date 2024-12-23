# Redis Priority Queue Implementation

A Python implementation of a priority queue using Redis as the backend storage. This implementation demonstrates how to handle tasks with different priority levels while ensuring each task is processed exactly once, even with multiple consumers.

## Features

- Priority-based task processing (1=high, 2=medium, 3=low)
- Multiple consumers can process tasks concurrently
- No duplicate processing of tasks
- Real-time task distribution
- Timestamps for task creation and processing
- Graceful shutdown handling

## Prerequisites

- Python 3.6+
- Redis server running on localhost:6379
- Python packages:
  ```
  redis
  ```

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/redis-priority-queue.git
   cd redis-priority-queue
   ```

2. Install dependencies:
   ```bash
   pip install redis
   ```

3. Ensure Redis server is running:
   ```bash
   # On macOS with Homebrew
   brew services start redis
   
   # On Ubuntu/Debian
   sudo service redis-server start
   ```

## Components

### 1. Redis Priority Queue (`redis_pq.py`)
- Core implementation of the priority queue using Redis sorted sets
- Provides push, pop, peek, and other queue operations
- Includes base classes for producers and consumers

### 2. Producer (`producer.py`)
- Generates tasks with random priorities and types
- Adds timestamps to track task flow
- Configurable production interval

### 3. Consumers (`consumer_1.py` and `consumer_2.py`)
- Process tasks based on priority
- Show timing information for task processing
- Different processing times to demonstrate load distribution

## Running the Demo

1. Start the producer in one terminal:
   ```bash
   python producer.py
   ```

2. Start the first consumer in another terminal:
   ```bash
   python consumer_1.py
   ```

3. Start the second consumer in a third terminal:
   ```bash
   python consumer_2.py
   ```

You'll see the following:
- Producer generating tasks with random priorities
- Tasks being distributed between consumers
- Each task processed exactly once
- Higher priority tasks processed before lower priority ones

To stop any component, press Ctrl+C in its terminal.

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

## How It Works

1. **Task Generation**:
   - Producer creates tasks with random priorities
   - Each task has a unique ID and timestamp
   - Tasks are pushed to Redis with priority as score

2. **Task Distribution**:
   - Redis sorted set maintains tasks ordered by priority
   - Lower score (higher priority) tasks are processed first
   - Multiple consumers can poll for tasks

3. **Task Processing**:
   - Consumers pop tasks from the queue
   - Each task is removed from Redis when popped
   - No task can be processed more than once
   - Consumers process tasks at different speeds

4. **Priority Handling**:
   - Priority 1 (High): Most urgent tasks
   - Priority 2 (Medium): Normal priority tasks
   - Priority 3 (Low): Background tasks

## Implementation Details

The priority queue is implemented using Redis sorted sets (ZSET):
- `ZADD` adds tasks with priority as score
- `ZRANGE` gets the highest priority task
- `ZREM` removes processed tasks
- Atomic operations ensure no duplicate processing

## Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.

## License

This project is licensed under the MIT License - see the LICENSE file for details.