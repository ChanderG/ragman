import chromadb
import subprocess
import tempfile

def index_page(collection, page):
    print(f"Indexing {page}...")

    with tempfile.NamedTemporaryFile(mode="w+") as fp:
        fname = fp.name
        # lifted from: https://superscript.com/blog/man-page-in-plain-text/
        command = f"man -P cat {page} | col -b > {fname}"

        subprocess.run(command, shell=True)

        data = fp.read()
        paras = data.split("\n\n")
        print("Obtained ", len(paras), " paras...")

    ids = list(map(lambda x: page+str(x), list(range(len(paras)))))
    collection.add(documents=paras, ids=ids)
