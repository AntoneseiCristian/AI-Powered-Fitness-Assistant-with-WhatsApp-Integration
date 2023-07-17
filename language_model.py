from gpt4all import GPT4All

model = GPT4All("C:/Users/Antonesei/AppData/Local/nomic.ai/GPT4All/ggml-model-gpt4all-falcon-q4_0.bin")

def get_response(prompt):
    output = model.generate(prompt, max_tokens=3)
    return output