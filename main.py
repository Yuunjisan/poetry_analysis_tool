from transformers import pipeline
from transformers.utils import logging

class PoetryAnalyzer:
    def __init__(self):
        logging.set_verbosity(40)
        self.poetry_model = pipeline("text-generation", model="meta-llama/Llama-3.2-1B-Instruct",
                    temperature=0.9,  # Higher temperature for more creative output
                    top_k=50,
                    top_p=0.95,
                    repetition_penalty=1.2,  # Avoid repetitive phrases
                    no_repeat_ngram_size=3,
                    do_sample=True,
                    max_new_tokens=450)

        self.emotion_model = pipeline("text-classification", model="SamLowe/roberta-base-go_emotions")

    @staticmethod
    def create_prompt(author=None, theme=None):
        if author and theme:
            return f"Please write a poem in the style of {author} about {theme}."
        if author:
            return f"Please write a poem in the style of {author}."
        if theme:
            return f"Please write a poem about {theme}."
        return "Please write a poem."

    def create_poem(self, author=None, theme=None):
        prompt = PoetryAnalyzer.create_prompt(author, theme)
        messages = [{"role": "user", "content": prompt}]
        poem = self.poetry_model(messages, pad_token_id=self.poetry_model.tokenizer.eos_token_id, return_text=True)[0]["generated_text"][1]["content"]

        # processing the poem by removing possible additions that are not part of the poem    
        for note_start_string in ["note that", "note:", "note -", "note :", "(", "note –"]:
            if note_start_string in poem.lower():
                end_note = poem.lower().find(note_start_string)
                last_enter = poem[:end_note].rfind("\n")
                # if there is no last enter just return until the note which might leave some ()
                if last_enter == -1:
                    return poem[:end_note]
                return poem[:last_enter]
        return poem

    def analyse_poem(self, poem):
        top_classes = self.emotion_model(poem, top_k=4)
        top_classes = list(filter(lambda x: x["label"] != "neutral", top_classes))[:3]
        return top_classes

    def __call__(self, author=None, theme=None):
        poem = self.create_poem(author, theme)
        analysis = self.analyse_poem(poem)
        return poem, analysis


def main():
    pa = PoetryAnalyzer()
    while True:
        author = input("Please enter an author: ")
        theme = input("Please enter a theme: ")
        poem, analysis = pa(author, theme)
        print(poem)
        print()
        print(analysis)
        print()

main()