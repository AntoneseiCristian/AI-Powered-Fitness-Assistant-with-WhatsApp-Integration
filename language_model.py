from gpt4all import GPT4All

model = GPT4All("C:/Users/anton/AppData/Local/nomic.ai/GPT4All/ggml-model-gpt4all-falcon-q4_0")

def get_response(prompt):
    output = model.generate(prompt, max_tokens=200, temp=0.7, top_k=40, top_p=0.1, repeat_penalty=1.18, repeat_last_n=64, n_batch=8, n_predict=None, streaming=False)
    if output.startswith(","):
        output = output[1:].strip()
    return output
