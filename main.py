import chromadb

def add_ls(collection):
    with open("pages/ls.txt", 'r') as f:
        data = f.read()
        paras = data.split("\n\n")
        print("Obtained ", len(paras), " paras...")

    ids = list(map(lambda x: "ls"+str(x), list(range(len(paras)))))
    collection.add(documents=paras, ids=ids)

def main():
    cl = chromadb.Client()

    collection = cl.create_collection(name="man")
    add_ls(collection)

    res = collection.query(query_texts=["How to reverse?"],
                           n_results=3)
    print(res)

if __name__ == "__main__":
    main()
