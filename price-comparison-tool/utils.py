from fuzzywuzzy import fuzz
from transformers import BertTokenizer, BertModel
import torch
from sklearn.metrics.pairwise import cosine_similarity

def is_similar(product_name, search_result):
    """
    Check if two product names are similar using fuzzy matching.
    """
    return fuzz.ratio(product_name.lower(), search_result.lower()) > 70

def encode_description(description):
    """
    Encode product description using BERT.
    """
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    model = BertModel.from_pretrained('bert-base-uncased')
    inputs = tokenizer(description, return_tensors='pt', truncation=True, padding=True)
    outputs = model(**inputs)
    return outputs.last_hidden_state.mean(dim=1).detach().numpy()

def is_same_product(description1, description2):
    """
    Compare two product descriptions using BERT embeddings.
    """
    embedding1 = encode_description(description1)
    embedding2 = encode_description(description2)
    similarity = cosine_similarity(embedding1, embedding2)
    return similarity[0][0] > 0.8  # Adjust threshold as needed