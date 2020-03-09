import boto3
import keyvalue.parsetriples as ParseTripe
import keyvalue.stemmer as Stemmer
import sys, getopt

dynamodb = boto3.resource('dynamodb')
dynamodbClient = boto3.client('dynamodb')

#This files modifies the put, get and select fucntions compared with sqlitekeyvalue.py

def put(table, keyword, inx, value):
    res = dynamodbClient.put_item(
        TableName = table,
        Item = {
            'keyword': {
                'S':keyword
            },
            'inx': {
                'N':inx
            },
            'value': {
                'S':value
            }
        }
    )
    return res 

def get(table, keyword, inx):
    res = dynamodbClient.get_item(
        TableName = table,
        Key = {
            'keyword':{
                'S':keyword
            },
            'inx':{
                'N':inx
            }
        }
    )
    return res

def store(num_imag):
    #Loading images and labels from file
    images = ParseTripe.ParseTriples("images.ttl")
    labels = ParseTripe.ParseTriples("labels_en.ttl")

    try: 
        imagesTable = dynamodbClient.describe_table(TableName="images")
    except dynamodbClient.exceptions.ResourceNotFoundException:
        imagesTable = createImagesTable('images')
    
    try: 
        labelsTable = dynamodbClient.describe_table(TableName="labels")
    except dynamodbClient.exceptions.ResourceNotFoundException:
        labelsTable = createImagesTable('labels')
    
    print(labelsTable)

    tempImages = {}
    num = int(num_imag)
    while(num > 0):
        line = images.getNext()
        if "depiction" in line[1]:
            if imagesTable.get(line[0]) is None:
                tempImages[line[0]] = 1
            else:
                tempImages[line[0]] += 1
            put('images', line[0], str(tempImages[line[0]]), line[2])
            num -= 1

    tag = {}

    label = labels.getNext()
    while(label):
        if label[1] == "http://www.w3.org/2000/01/rdf-schema#label" and label[0] in imagesTable:
            #label[0] in imagesTable:
            labelsTable = label[2].split(" ")
            for entry in labelsTable:
                #Save stem word
                entry = Stemmer.stem(entry)
                #if there is already an entry with the same label then increases the sort value
                if tag.get(entry) is None:
                    tag[entry] =  0
                else:
                    tag[entry] += 1
                #save sort word: table, keyword, inx and value
                put('labels', entry, str(tag[entry]), label[0])
        label = labels.getNext()

    
def createImagesTable(name):
    table = dynamodb.create_table(
        TableName = name,
        KeySchema = [
            {
                'AttributeName': 'keyword',
                'KeyType': 'HASH'
            },
            {
                'AttributeName': 'inx', #sort key
                'KeyType': 'RANGE'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'keyword',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'inx',
                'AttributeType': 'N'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )
    table.meta.client.get_waiter('table_exists').wait(TableName=name)
    return table



def main(argv):
    sys.argv.pop(0)
    store(sys.argv[0])

if __name__ == "__main__":
    main(sys.argv[1:])