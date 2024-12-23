from redis.asyncio import Redis
import json
import time
import signal
import asyncio
import random
from datetime import datetime
from typing import Any, Optional, List, Callable
from abc import ABC, abstractmethod

class RedisPriorityQueue:
    def __init__(self, host='localhost', port=6379, db=0):
        """Initialize Redis priority queue.
        
        Args:
            host (str): Redis host address
            port (int): Redis port number
            db (int): Redis database number
        """
        self.redis_client = None
        self.host = host
        self.port = port
        self.db = db
        
    async def connect(self):
        """Connect to Redis server"""
        self.redis_client = Redis(
            host=self.host,
            port=self.port,
            db=self.db
        )
        
    async def disconnect(self):
        """Disconnect from Redis server"""
        if self.redis_client:
            await self.redis_client.close()
            
    async def push(self, queue_name: str, data: Any, priority: int = 0) -> bool:
        """Push an item onto the priority queue.
        
        Args:
            queue_name (str): Name of the queue
            data (Any): Data to be stored
            priority (int): Priority level (lower number = higher priority)
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            item = {
                'data': data,
                'timestamp': datetime.utcnow().isoformat(),
            }
            
            # Use ZADD to add item to sorted set with priority as score
            return await self.redis_client.zadd(
                queue_name,
                {json.dumps(item): priority}
            )
        except Exception as e:
            print(f"Error pushing to queue: {e}")
            return False
            
    async def pop(self, queue_name: str) -> Optional[dict]:
        """Pop the highest priority item from the queue.
        
        Args:
            queue_name (str): Name of the queue
            
        Returns:
            Optional[dict]: Item with highest priority or None if queue is empty
        """
        try:
            # Get the item with lowest score (highest priority)
            items = await self.redis_client.zrange(queue_name, 0, 0)
            
            if not items:
                return None
                
            # Remove the item from the queue
            await self.redis_client.zrem(queue_name, items[0])
            
            # Parse and return the item
            return json.loads(items[0])
        except Exception as e:
            print(f"Error popping from queue: {e}")
            return None
            
    async def peek(self, queue_name: str) -> Optional[dict]:
        """Look at the highest priority item without removing it.
        
        Args:
            queue_name (str): Name of the queue
            
        Returns:
            Optional[dict]: Item with highest priority or None if queue is empty
        """
        try:
            items = await self.redis_client.zrange(queue_name, 0, 0)
            return json.loads(items[0]) if items else None
        except Exception as e:
            print(f"Error peeking queue: {e}")
            return None
            
    async def length(self, queue_name: str) -> int:
        """Get the current length of the queue.
        
        Args:
            queue_name (str): Name of the queue
            
        Returns:
            int: Number of items in the queue
        """
        return await self.redis_client.zcard(queue_name)
        
    async def get_all(self, queue_name: str) -> List[dict]:
        """Get all items in the queue ordered by priority.
        
        Args:
            queue_name (str): Name of the queue
            
        Returns:
            List[dict]: All items in priority order
        """
        try:
            items = await self.redis_client.zrange(queue_name, 0, -1)
            return [json.loads(item) for item in items]
        except Exception as e:
            print(f"Error getting all items: {e}")
            return []

class BaseWorker(ABC):
    """Base class for Producer and Consumer workers"""
    
    def __init__(self, queue: RedisPriorityQueue, queue_name: str):
        self.queue = queue
        self.queue_name = queue_name
        self.running = False
        self.loop = None
        
    def handle_signal(self, signum, frame):
        """Handle shutdown signals"""
        print(f"\nReceived signal {signum}. Shutting down...")
        self.running = False
        
    async def start(self):
        """Start the worker"""
        # Set up signal handling
        signal.signal(signal.SIGINT, self.handle_signal)
        signal.signal(signal.SIGTERM, self.handle_signal)
        
        self.running = True
        self.loop = asyncio.get_running_loop()
        await self.queue.connect()
        await self.run()
        await self.queue.disconnect()
            
    @abstractmethod
    async def run(self):
        """Main worker loop - must be implemented by subclasses"""
        pass

class Producer(BaseWorker):
    """Producer class to generate and push items to the queue"""
    
    def __init__(self, queue: RedisPriorityQueue, queue_name: str, 
                 item_generator: Callable[[], tuple[Any, int]], 
                 interval: float = 1.0):
        """
        Args:
            queue (RedisPriorityQueue): Queue instance
            queue_name (str): Name of the queue
            item_generator (Callable): Function that returns (data, priority) tuples
            interval (float): Time between producing items in seconds
        """
        super().__init__(queue, queue_name)
        self.item_generator = item_generator
        self.interval = interval
        
    async def run(self):
        """Main producer loop"""
        while self.running:
            try:
                # Generate new item and priority
                data, priority = self.item_generator()
                
                # Push to queue
                success = await self.queue.push(self.queue_name, data, priority)
                
                if success:
                    print(f"Produced item: {data} with priority {priority}")
                else:
                    print("Failed to produce item")
                    
                # Wait before producing next item
                await asyncio.sleep(self.interval)
                
            except Exception as e:
                print(f"Error in producer: {e}")
                await asyncio.sleep(1)  # Wait before retrying

class Consumer(BaseWorker):
    """Consumer class to process items from the queue"""
    
    def __init__(self, queue: RedisPriorityQueue, queue_name: str, 
                 item_processor: Callable[[dict], None], 
                 poll_interval: float = 1.0):
        """
        Args:
            queue (RedisPriorityQueue): Queue instance
            queue_name (str): Name of the queue
            item_processor (Callable): Function that processes items from queue
            poll_interval (float): Time between queue checks when empty
        """
        super().__init__(queue, queue_name)
        self.item_processor = item_processor
        self.poll_interval = poll_interval
        
    async def run(self):
        """Main consumer loop"""
        while self.running:
            try:
                # Try to get an item from the queue
                item = await self.queue.pop(self.queue_name)
                
                if item:
                    # Process the item
                    print(f"Processing item: {item}")
                    await self.item_processor(item)
                else:
                    # If queue is empty, wait before checking again
                    await asyncio.sleep(self.poll_interval)
                    
            except Exception as e:
                print(f"Error in consumer: {e}")
                await asyncio.sleep(1)  # Wait before retrying
