from redis_pq import RedisPriorityQueue, Consumer
import time

def process_task(item):
    """Process tasks and show timing information"""
    task_data = item['data']
    current_time = time.strftime("%H:%M:%S")
    
    print(f"\n[Consumer 1 at {current_time}] Got task:")
    print(f"  - Task ID: {task_data['task_id']}")
    print(f"  - Created at: {task_data['created_at']}")
    print(f"  - Type: {task_data['task_type']}")
    print(f"  - Priority: {task_data['priority_level']}")
    print(f"  - Payload: {task_data['payload']}")
    
    # Simulate processing
    time.sleep(1.5)
    print(f"[Consumer 1] Completed task {task_data['task_id']}\n")

if __name__ == "__main__":
    # Initialize queue
    queue = RedisPriorityQueue(host='localhost', port=6379, db=0)
    
    # Create consumer with 0.5 second polling interval
    consumer = Consumer(
        queue=queue,
        queue_name="task_queue",
        item_processor=process_task,
        poll_interval=0.5
    )
    
    print("Starting Consumer 1...")
    print("This consumer will process tasks as they come in.")
    print("Notice that each task is processed exactly once between the consumers.")
    
    try:
        consumer.start()
        # Keep the main thread alive
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down Consumer 1...")
        consumer.stop() 