import click
import os
import chromadb

from .core import index_page

@click.group()
def cli():
    pass

@cli.command()
@click.argument("page")
@click.argument("query")
def search(page, query):

    # check for the db
    cl = chromadb.PersistentClient(path=os.path.expanduser("~/.config/ragman/db.chroma"))

    try:
        col = cl.get_collection(name="man-"+page)
    except chromadb.errors.NotFoundError as e:
        col = cl.create_collection(name="man-"+page)
        index_page(col, page)

    res = col.query(query_texts=[query], n_results = 3)

    # since query is an array of strings
    # response too has a 2d array

    print(10*"====")
    for entry in res['documents'][0]:
        print(entry)
        print("\n" + 10*"====")
