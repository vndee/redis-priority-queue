from redis_pq import RedisPriorityQueue, Consumer
import time
import asyncio

async def process_task(item):
    """Process tasks and show timing information"""
    task_data = item['data']
    current_time = time.strftime("%H:%M:%S")
    
    print(f"\n[Consumer 2 at {current_time}] Got task:")
    print(f"  - Task ID: {task_data['task_id']}")
    print(f"  - Created at: {task_data['created_at']}")
    print(f"  - Type: {task_data['task_type']}")
    print(f"  - Priority: {task_data['priority_level']}")
    print(f"  - Payload: {task_data['payload']}")
    
    # Simulate processing with longer time
    await asyncio.sleep(2.0)
    print(f"[Consumer 2] Completed task {task_data['task_id']}\n")

async def main():
    # Initialize queue
    queue = RedisPriorityQueue(host='localhost', port=6379, db=0)
    
    # Create consumer with 0.5 second polling interval
    consumer = Consumer(
        queue=queue,
        queue_name="task_queue",
        item_processor=process_task,
        poll_interval=0.5
    )
    
    print("Starting Consumer 2...")
    print("This consumer will process tasks as they come in.")
    print("Notice that each task is processed exactly once between the consumers.")
    
    await consumer.start()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nShutting down Consumer 2...")
