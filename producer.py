from redis_pq import RedisPriorityQueue, Producer
import random
import time

def generate_mixed_priority_task():
    """Generate tasks with different priorities"""
    # Randomly choose task type and priority
    task_type = random.choice(["email", "notification", "report", "backup"])
    priority = random.randint(1, 3)  # 1=high, 2=medium, 3=low
    priority_levels = {1: "high", 2: "medium", 3: "low"}
    
    data = {
        "task_id": random.randint(1000, 9999),
        "task_type": task_type,
        "priority_level": priority_levels[priority],
        "created_at": time.strftime("%H:%M:%S"),
        "payload": f"{priority_levels[priority].capitalize()} priority {task_type} task"
    }
    return data, priority

if __name__ == "__main__":
    # Initialize queue
    queue = RedisPriorityQueue(host='localhost', port=6379, db=0)
    
    # Create producer with 1 second interval
    producer = Producer(
        queue=queue,
        queue_name="task_queue",
        item_generator=generate_mixed_priority_task,
        interval=1.0
    )
    
    print("Starting Producer (Mixed Priority Tasks)...")
    print("This producer will generate tasks with different priorities:")
    print("- Priority 1 (High)")
    print("- Priority 2 (Medium)")
    print("- Priority 3 (Low)")
    producer.start()
    
    try:
        # Keep the main thread alive
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down Producer...")
        producer.stop() 