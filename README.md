# ragman

Simple RAG setup for man pages.

## Scope

This is a simple one-off tool with limited scope of querying/rag with man pages. It is also purposefully limited in complexity to serve as a good first-point learning exercise.

Only tested to work on Linux. No GPUs required.

## Install

```
pip install pip@git+https://github.com/ChanderG/ragman
```

## Use

Ragman has just 2 commands.

### Query

Query for top 3 semantically matching paragraphs in the relevant man page.

```
ragman search bash "How to list jobs?"
```

This will simply bring out the top 3 relevant paragraphs from the man page of bash.

### Chat

Instead:
```
ragman chat bash "How to list jobs?"
```
will obtain the relevant context, form a query of all this and send to an LLM for completion.

To run this, you need to set the following env variables:
1. `OPENAI_BASE_URL` to a suitable endpoint (could be an `ollama` endpoint)
2. `OPENAI_API_KEY` to your key (not needed if using `ollama`).
3. Set the model using `-m` flag to the `chat` subcommand.

## How does it work?

Very simple internals.
1. We use Chromadb as the Vector store.
2. We index documents (ie the man pages) once on first usage. This strategy works since man pages are static entries (and will not work for other use-cases like RAG on code-bases which will keep changing.)
3. We split man pages into paragraphs. Each para is a chunk that is embedded separately. This is not the best chunking strategy out there (we don't do overlaps for example, or discover real context boundaries using NLP techniques), but it is passable for this demo.
4. We use the default Chromadb embedding model, which happens to be `all-MiniLM-L6-v2`, which happens to run fas enough on CPUs (at least for the small documents sizes of man pages).
5. We use OpenAI API to make the Generation call. This has become a reasonable standard, supported by many other providers including Ollama and vLLM.

## License 
MIT
