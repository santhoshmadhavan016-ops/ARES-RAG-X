import requests


class LLM:

    def __init__(self):
        self.url = "http://localhost:11434/api/generate"
        self.model = "llama3.2:3b"

    def generate(self, prompt):

        response = requests.post(
            self.url,
            json={
                "model": self.model,
                "prompt": prompt,
                "stream": False
            }
        )

        response.raise_for_status()

        data = response.json()

        return data["response"]


if __name__ == "__main__":

    llm = LLM()

    answer = llm.generate(
        "What is Retrieval Augmented Generation (RAG)? "
        "Explain it in 2 simple sentences."
    )

    print("\nLLM RESPONSE")
    print("=" * 60)
    print(answer)