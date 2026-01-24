import pandas as pd
import numpy as np
import re
import pickle
import torch
from datasets import load_dataset
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from collections import Counter

def clean_text(text):
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def tokenize(text, word_to_idx, max_len):
    tokens = text.split()
    indexed = [word_to_idx.get(token, 1) for token in tokens] # 1 for <UNK>
    if len(indexed) < max_len:
        indexed += [0] * (max_len - len(indexed)) # 0 for <PAD>
    else:
        indexed = indexed[:max_len]
    return indexed

def prepare_data(max_words=10000, max_len=100):
    print("Loading dataset...")
    dataset = load_dataset("Tobi-Bueck/customer-support-tickets")
    df = pd.DataFrame(dataset['train'])
    
    print("Preprocessing text...")
    df['body'] = df['body'].apply(clean_text)
    
    # Filter out empty or very short bodies
    df = df[df['body'].str.len() > 10]
    
    # We might want to limit to top queues if 52 is too many, but let's try to keep the most frequent ones
    top_queues = df['queue'].value_counts().nlargest(10).index.tolist()
    print(f"Top 10 queues: {top_queues}")
    df = df[df['queue'].isin(top_queues)]
    
    print("Encoding labels...")
    le = LabelEncoder()
    df['queue_encoded'] = le.fit_transform(df['queue'])
    
    print("Building vocabulary...")
    all_words = " ".join(df['body']).split()
    word_counts = Counter(all_words)
    most_common_words = [word for word, count in word_counts.most_common(max_words)]
    word_to_idx = {word: i+2 for i, word in enumerate(most_common_words)}
    word_to_idx["<PAD>"] = 0
    word_to_idx["<UNK>"] = 1
    
    print("Tokenizing...")
    df['tokenized'] = df['body'].apply(lambda x: tokenize(x, word_to_idx, max_len))
    
    X = np.array(df['tokenized'].tolist())
    y = np.array(df['queue_encoded'].tolist())
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Save artifacts
    with open('backend/training/tokenizer.pkl', 'wb') as f:
        pickle.dump(word_to_idx, f)
    with open('backend/training/label_encoder.pkl', 'wb') as f:
        pickle.dump(le, f)
        
    return X_train, X_test, y_train, y_test, len(word_to_idx), len(top_queues), max_len

if __name__ == "__main__":
    prepare_data()
