# Embeddings:

From [OpenAI Cookbook](https://cookbook.openai.com/examples/question_answering_using_embeddings):


> 1. Prepare search data (once per document)
>   1. Collect: We'll download a few hundred Wikipedia articles about the 2022 Olympics
>   2. Chunk: Documents are split into short, mostly self-contained sections to be embedded
>   3. Embed: Each section is embedded with the OpenAI API
>   4. Store: Embeddings are saved (for large datasets, use a vector database)
> 2. Search (once per query)
>   1. Given a user question, generate an embedding for the query from the OpenAI API
>   2. Using the embeddings, rank the text sections by relevance to the query
> 3. Ask (once per query)
>   1. Insert the question and the most relevant sections into a message to GPT
>   2. Return GPT's answer

## Memory and Feelings

- need to store text AND embedding array, not just embeddings??
- maybe mutate it after finding the correct memory.
