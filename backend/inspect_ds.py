from datasets import load_dataset

def inspect_dataset():
    print("Loading dataset...")
    ds = load_dataset('Tobi-Bueck/customer-support-tickets')
    
    # Assuming 'train' split exists, if not we'll list splits
    split = 'train' if 'train' in ds else list(ds.keys())[0]
    data = ds[split]
    
    print(f"\nColumn names: {data.column_names}")
    
    print("\nExamples (body and queue):")
    for i in range(min(3, len(data))):
        body = data[i].get('body', 'N/A')
        queue = data[i].get('queue', 'N/A')
        print(f"Example {i+1}:")
        print(f"  Body: {body[:150]}...")
        print(f"  Queue: {queue}")
    
    if 'queue' in data.column_names:
        unique_queues = set(data['queue'])
        print(f"\nUnique values in 'queue' ({len(unique_queues)}):")
        for q in sorted(list(unique_queues)):
            print(f"  - {q}")
    else:
        print("\n'queue' column not found.")

if __name__ == "__main__":
    inspect_dataset()
