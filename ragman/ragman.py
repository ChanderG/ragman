import click
import os
import chromadb
from openai import OpenAI

from .core import index_page

@click.group()
def cli():
    pass

def get_collection(page):
    # check for the db
    cl = chromadb.PersistentClient(path=os.path.expanduser("~/.config/ragman/db.chroma"))

    try:
        col = cl.get_collection(name="man-"+page)
    except chromadb.errors.NotFoundError as e:
        col = cl.create_collection(name="man-"+page)
        index_page(col, page)

    return col

@cli.command()
@click.argument("page")
@click.argument("query")
def search(page, query):
    col = get_collection(page)
    res = col.query(query_texts=[query], n_results = 3)

    # since query is an array of strings
    # response too has a 2d array

    print(10*"====")
    for entry in res['documents'][0]:
        print(entry)
        print("\n" + 10*"====")

@cli.command()
@click.argument("page")
@click.argument("query")
def chat(page, query):
    col = get_collection(page)
    res = col.query(query_texts=[query], n_results = 3)

    msg = f"Given the following context, answer the final question for the command {page}."
    for entry in res['documents'][0]:
        msg += entry
        msg += "\n"
    msg += query

    client = OpenAI()

    completion = client.chat.completions.create(
        model="ibm-granite/granite-3.1-8b-instruct",
        messages=[{"role": "user", "content": msg}])

    print(completion.choices[0].message.content)
