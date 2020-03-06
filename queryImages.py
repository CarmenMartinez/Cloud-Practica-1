import keyvalue.sqlitekeyvalue as KeyValue
import keyvalue.parsetriples as ParseTripe
import keyvalue.stemmer as Stemmer
import sys


# Make connections to KeyValue
kv_labels = KeyValue.SqliteKeyValue("sqlite_labels.db","labels",sortKey=True)
kv_images = KeyValue.SqliteKeyValue("sqlite_images.db","images")

# Process Logic.
def getImages(params):
    print(params)
    for p in params:
        p = Stemmer.stem(p)
        tags = kv_labels.getAll(p)
        for t in tags:
            images = kv_images.get(t[0])
            print(images)
    # Close KeyValues Storages
    kv_labels.close()
    kv_images.close()

def main(argv):
    getImages(argv)


if __name__ == "__main__":
   main(sys.argv[1:])










