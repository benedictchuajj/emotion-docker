import torch
from transformers import DistilBertTokenizer, DistilBertModel
import torch.nn.functional as F

"""
Wrapper class of the Emotion Analysis DistilBERT model. 
Trained on a simplified version of the Emotions dataset.

Possible Enhancements:
- Write a config file to indicate model type to use.
"""

## Config
encode_dict = {0: 'anger', 1: 'joy', 2: 'others', 3: 'sadness'}
model_path = "models/DISTILBERT_ekman_epoch_4.model"
vocab_path = "models/DISTILBERT_vocab_ekman_epoch_4.model"

base_model_name = 'distilbert-base-uncased'
device = "cuda" if torch.cuda.is_available() else "cpu"

class DistillBERTClass(torch.nn.Module): 
    def __init__(self): 
        super(DistillBERTClass, self).__init__() 
        self.l1 = DistilBertModel.from_pretrained(base_model_name) 
        self.pre_classifier = torch.nn.Linear(768, 768) 
        self.dropout = torch.nn.Dropout(0.3) 
        self.classifier = torch.nn.Linear(768, len(encode_dict)) 

    def forward(self, input_ids, attention_mask): 
        output_1 = self.l1(input_ids=input_ids, attention_mask=attention_mask) 
        hidden_state = output_1[0] 
        pooler = hidden_state[:, 0] 
        pooler = self.pre_classifier(pooler) 
        pooler = torch.nn.ReLU()(pooler) 
        pooler = self.dropout(pooler) 
        output = self.classifier(pooler) 
        return output
    
class SimpleEmotionsModel:
    def __init__(self):
        self.model = DistillBERTClass()
        self.model.to(device)
        self.model.load_state_dict(torch.load(model_path, map_location=torch.device('cpu')))
        
        self.tokenizer = DistilBertTokenizer.from_pretrained(vocab_path)
        self.encode_dict = encode_dict

    def predict(self, sentence):
        tokens = self.tokenizer.encode_plus(
            sentence,
            add_special_tokens=True,
            max_length=512,
            truncation=True,
            padding='longest',
            return_tensors='pt'
        )

        input_ids = tokens['input_ids']
        attention_mask = tokens['attention_mask']

        # Ensure the model is in evaluation mode
        self.model.eval()

        # Forward pass
        with torch.no_grad():
            outputs = self.model(input_ids=input_ids, attention_mask=attention_mask)

        # Format output
        probabilities = F.softmax(outputs)
        topk_values, topk_indices = torch.topk(probabilities[0], k=4)
        predictions_list = []

        for value, index in zip(topk_values, topk_indices):
            prediction = {'name': self.encode_dict[index.item()], 'value': value.item()}
            predictions_list.append(prediction)

        return predictions_list
    