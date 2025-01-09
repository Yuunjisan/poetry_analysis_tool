from flask import Flask, request, jsonify
from flask_cors import CORS
from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers import pipeline
import torch

app = Flask(__name__)
CORS(app)

class PoetryGenerator:
    def __init__(self):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        print(f"Using device: {self.device}")

        print("Loading poetry generation model...")
        self.model_name = "mehwish67/poem_Generator"
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForCausalLM.from_pretrained(self.model_name).to(self.device)
        
        print("Loading emotion analysis model...")
        self.emotion_analyzer = pipeline(
            "text-classification",
            model="j-hartmann/emotion-english-distilroberta-base",
            return_all_scores=True,
            device=0 if torch.cuda.is_available() else -1
        )
        print("All models loaded!")

    def preprocess_prompt(self, theme):
        """
        Preprocess the prompt to match the model's training format.
        The model was trained on poetry with themes, so we format accordingly.
        """
        # Format the theme to match training data style
        formatted_theme = theme.lower().strip()
        # Create a prompt that matches the training data format
        prompt = f"<|startoftext|>\nTheme: {formatted_theme}\n\n"
        return prompt

    def generate_poem(self, theme, max_length=200):
        try:
            # Preprocess the input
            input_text = self.preprocess_prompt(theme)
            print(f"Preprocessed prompt: {input_text}")
            
            # Tokenize input
            inputs = self.tokenizer(input_text, return_tensors='pt').to(self.device)
            
            # Generate with sampling parameters tuned for poetry
            outputs = self.model.generate(
                inputs["input_ids"],
                max_length=max_length,
                num_return_sequences=1,
                temperature=0.9,  # Higher temperature for more creative output
                top_k=50,
                top_p=0.95,
                repetition_penalty=1.2,  # Avoid repetitive phrases
                no_repeat_ngram_size=3,
                pad_token_id=self.tokenizer.eos_token_id,
                do_sample=True,
                eos_token_id=self.tokenizer.encode("<|endoftext|>")[0]
            )
            
            # Decode and clean up the generated text
            generated_poem = self.tokenizer.decode(outputs[0], skip_special_tokens=False)
            # Remove special tokens and clean up
            final_poem = generated_poem.replace("<|startoftext|>", "").replace("<|endoftext|>", "")
            final_poem = final_poem.replace(f"Theme: {theme}\n\n", "").strip()
            
            print(f"Generated poem preview: {final_poem[:100]}...")
            return final_poem
            
        except Exception as e:
            print(f"Error in generate_poem: {str(e)}")
            raise

    def analyze_emotions(self, poem):
        try:
            # Analyze emotions for the whole poem
            emotions = self.emotion_analyzer(poem)[0]
            emotion_dict = {item['label']: item['score'] for item in emotions}
            return emotion_dict
        except Exception as e:
            print(f"Error in analyze_emotions: {str(e)}")
            raise

# Initialize the generator
generator = PoetryGenerator()

@app.route('/generate', methods=['POST'])
def generate():
    try:
        data = request.json
        print(f"Received request data: {data}")
        
        theme = data.get('theme', '')
        
        if not theme:
            return jsonify({'error': 'Theme must be specified'}), 400
            
        print(f"Generating poem with theme: {theme}")
        
        # Generate poem
        poem = generator.generate_poem(theme)
        
        if not poem:
            return jsonify({'error': 'Failed to generate poem'}), 500
            
        # Analyze emotions
        emotions = generator.analyze_emotions(poem)
            
        return jsonify({
            'poem': poem,
            'emotions': emotions
        })
        
    except Exception as e:
        print(f"Error in generate endpoint: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)