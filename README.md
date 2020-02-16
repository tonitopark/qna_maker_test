# qna_maker_test

# pre-requisites
- Install QnA Maker
 ```
 pip install azure-cognitiveservices-knowledge-qnamaker
 ```

 - create environmnet variables
``` 
export COGNITIVE_SERVICE_KEY=my-key
```


# Object model

## Initialization
 
-  [CognitveServicesCredentials(subscription_key)](https://docs.microsoft.com/en-us/python/api/msrest/msrest.authentication.cognitiveservicescredentials?view=azure-python) 

- [QnAMakerClient(endpoint,credentials)](https://docs.microsoft.com/en-us/python/api/azure-cognitiveservices-knowledge-qnamaker/azure.cognitiveservices.knowledge.qnamaker.qnamakerclient?view=azure-python)

## Create, mamange and publish

- [KnowledgebaseOperations(client,config,serializer,deserializer)](https://docs.microsoft.com/en-us/python/api/azure-cognitiveservices-knowledge-qnamaker/azure.cognitiveservices.knowledge.qnamaker.operations.knowledgebaseoperations?view=azure-python)

## [Status](https://docs.microsoft.com/en-us/python/api/azure-cognitiveservices-knowledge-qnamaker/azure.cognitiveservices.knowledge.qnamaker.models.operationstatetype?view=azure-python) Handling

 - Immediate operations returns a JSON object
 - Long-running operations returns operation ID
    - [client.Operations.getDetails](https://docs.microsoft.com/en-us/python/api/azure-cognitiveservices-knowledge-qnamaker/azure.cognitiveservices.knowledge.qnamaker.operations.operations(class)?view=azure-python#get-details-operation-id--custom-headers-none--raw-false----operation-config-)