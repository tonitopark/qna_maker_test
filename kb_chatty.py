import os
import time
import json
from azure.cognitiveservices.knowledge.qnamaker import QnAMakerClient
from azure.cognitiveservices.knowledge.qnamaker.models import QnADTO, MetadataDTO, CreateKbDTO, OperationStateType, UpdateKbOperationDTO, UpdateKbOperationDTOAdd
from msrest.authentication import CognitiveServicesCredentials

# Check credentials
key_var_name = 'QNAMAKER_KEY'
if not key_var_name in os.environ:
    raise Exception('Please set/export the environment variable: {}'.format(key_var_name))
subscription_key = os.environ[key_var_name]

host_var_name = 'QNAMAKER_HOST'
if not host_var_name in os.environ:
    raise Exception('Please set/export the environment variable: {}'.format(host_var_name))
host = os.environ[host_var_name]

# Define utility function for status monitoring
# Helper functions
def _monitor_operation(client, operation):

    for i in range(1000):
        if operation.operation_state in [OperationStateType.not_started, OperationStateType.running]:
            print("Waiting for operation: {} to complete.".format(operation.operation_id))
            time.sleep(5)
            operation = client.operations.get_details(operation_id=operation.operation_id)
        else:
            break
    if operation.operation_state != OperationStateType.succeeded:
        raise Exception("Operation {} failed to complete.".format(operation.operation_id))
    return operation

    

client = QnAMakerClient(endpoint=host, credentials=CognitiveServicesCredentials(subscription_key))


#Load Chatty data
with open('faq_all.json') as f:
    data = json.load(f)

new_data = []
for item in data:
    if not isinstance(item['question'],float):
        new_data.append(item)

#intent-descrption dict
with open('intent_description.json') as g:
    desc = json.load(g)
    intdict=dict()
for item in desc:
    intdict[item[0]]=item[1]


def create_kb(client):


    qna = []
    record = new_data[0]
    qna.append(
        QnADTO(
            answer = intdict[record['intent']],
            questions = [record['question']],
            metadata = [MetadataDTO(name='Intent',value=record['intent'])]
                        #MetadataDTO(name='AdminTag',value=record['admin_tag'])]
        )
    )


    create_kb_dto = CreateKbDTO(
        name = "SKT Chatty FAQ",
        qna_list = qna,
        urls=None #urls
    )
    create_op = client.knowledgebase.create(create_kb_payload=create_kb_dto)
    
    create_op = _monitor_operation(client=client, operation=create_op)

    return create_op.resource_location.replace("/knowledgebases/", "")

# # create kb
kb_id = create_kb(client)
print(kb_id)


def publish_kb(client, kb_id):
    client.knowledgebase.publish(kb_id=kb_id)



# Publish the KB
print("Publishing KB...")
publish_kb (client=client, kb_id=kb_id)
print("KB Published.")
print()


def update_kb(client, kb_id,record):

    qna = []
    
    qna.append(
        QnADTO(
            answer = intdict[record['intent']],
            questions = [record['question']],
            metadata = [MetadataDTO(name='Intent',value=record['intent'])]
                        #MetadataDTO(name='AdminTag',value=record['admin_tag'])]
        )
    )

    update_kb_operation_dto = UpdateKbOperationDTO(
        add=UpdateKbOperationDTOAdd(
            qna_list=qna
        )
    )
    update_op = client.knowledgebase.update(kb_id=kb_id, update_kb=update_kb_operation_dto)
    _monitor_operation(client=client, operation=update_op)


# Update a KB
for idx, record in enumerate(new_data[1:]):
    print("Updating KB...")
    update_kb (client=client, kb_id=kb_id,record=record)
    print("KB Updated.")
print()

