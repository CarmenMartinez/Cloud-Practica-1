import keyvalue.sqlitekeyvalue as KeyValue
import keyvalue.parsetriples as ParseTripe
import keyvalue.stemmer as Stemmer


# Make connections to KeyValue
kv_labels = KeyValue.SqliteKeyValue("sqlite_labels.db","labels",sortKey=True)
kv_images = KeyValue.SqliteKeyValue("sqlite_images.db","images")

# Process Logic.

#reading ttl files
images = ParseTripe.ParseTriples("images.ttl")

#setting a limit of 100 images to load
i = 0
while (i <= 400):
    image = images.getNext()
    #filter if the image is not a thumbnail
    if "depiction" in image[1]:
       kv_images.put(image[0], image[2])
       #i only increases if the image is not a thumbnail
       i += 1

labels = ParseTripe.ParseTriples("labels_en.ttl")
label = labels.getNext()

tag = {}
while(label):
    #Check if the image on the label is inside of the kv_images
    if kv_images.get(label[0]):
        #separate labels for each word
        entries = label[2].split(" ")
        for entry in entries:
            #Save stem word
            entry = Stemmer.stem(entry)
            #if there is already an entry with the same label then increases the sort value
            if tag.get(entry) is None:
                tag[entry] =  0
            else:
                tag[entry] += 1
            #save sort word
            kv_labels.putSort(entry, str(tag[entry]), label[0])
    label = labels.getNext()



# Close KeyValues Storages
kv_labels.close()
kv_images.close()







