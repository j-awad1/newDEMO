import boto3
import json
import Utils

class BedrockProcessing():
    def __init__(self):
        self.bedrock_agent = boto3.client('bedrock-agent')
        self.bedrock_agent_runtime = boto3.client('bedrock-agent-runtime')
        self.bedrock_runtime = boto3.client('bedrock-runtime')
        self.modelId = "anthropic.claude-3-sonnet-20240229-v1:0"
        #self.modelId = "meta.llama2-70b-chat-v1"

    def get_knowledge_response_using_pagination(self, prompt):
        paginator = self.bedrock_agent_runtime.get_paginator('retrieve')
        response_iterator = paginator.paginate(
            knowledgeBaseId=self.get_knowledgebase_id(),
            retrievalQuery={
                            'text': prompt
                            }
        )
        kb_response=[]
        kb_location=[]
        for response in response_iterator:
                for result in response['retrievalResults']:
                    #print(result)
                    #print("*"*100)
                    k_t=result['content']['text']
                    kb_location.append(result['location'])
                    kb_response.append(k_t)
        
        knowledgebase_response = ''.join(kb_response)
        r1= Utils.remove_duplicates(kb_location)
        return {"prompt":knowledgebase_response,"location":r1}
                

    def get_knowledgebase_id(self):
        response = self.bedrock_agent.list_knowledge_bases()
        response['knowledgeBaseSummaries']
        # knowledgeBaseId = response['knowledgeBaseSummaries'][0]['knowledgeBaseId']
        # print('kbid ', knowledgeBaseId)
        knowledgeBaseId ='5SU5QIYQEN' #5SU5QIYQEN flood - no flood:5YNN8CLAS8

        return knowledgeBaseId
    
    def get_knowledgebase_response(self, prompt):
        response = self.bedrock_agent_runtime.retrieve(knowledgeBaseId=self.get_knowledgebase_id(), retrievalQuery={
                                    'text': prompt}
                                  )
        for result in response['retrievalResults']:
            #print(result['content']['text'])
            knowledge_text = result['content']['text']
        return(knowledge_text)
 
    
    
    def get_response_from_bedrock_model_llama2(self, prompt):
        max_gen_len = 128
        temperature = 0.1
        top_p = 0.9
        model_id='meta.llama2-70b-chat-v1'
        accept = "application/json"
        content_type = "application/json"
    
        # Create request body.
        body = json.dumps({
            "prompt": prompt,
            "max_gen_len": max_gen_len,
            "temperature": temperature,
            "top_p": top_p
        })
    
        response = self.bedrock_runtime.invoke_model(
            body=body, modelId=model_id, accept=accept, contentType=content_type
        )
    
        response_body = json.loads(response.get('body').read())
        return response_body['generation']
 

    def get_response_from_bedrock_model_claude3(self,prompt):
        model_id= "anthropic.claude-3-sonnet-20240229-v1:0"
        body=json.dumps(
                    {
                        "anthropic_version": "bedrock-2023-05-31",
                        "max_tokens": 4096,
                        "temperature": 0.3,
                        "top_p": 0.8,
                        "messages": [
                            {
                                "role": "user",
                                "content": [{"type": "text", "text": prompt}],
                            }
                        ],
                    }
                )

        response = self.bedrock_runtime.invoke_model(
                                                            body=body, #tab'bytes'|file,
                                                            contentType='application/json',
                                                            accept='application/json',
                                                            modelId= model_id
                                                        )
        response_body = json.loads(response.get('body').read())
        #print(response_body)
        #print(type(references))
        return(response_body.get("content")[0]['text'])
     
    def get_response_from_bedrock_model_mistral(self, prompt):
        model_id='mistral.mistral-7b-instruct-v0:2'
        accept = 'application/json'
        content_type = 'application/json'
        
        # Create request body.
        body = json.dumps({
            "prompt": prompt,
            "max_tokens": 2048,
            "temperature": 0.3,
            "top_p": 0.8
        })
        
        
        response = self.bedrock_runtime.invoke_model(
                                                            body=body, #tab'bytes'|file,
                                                            contentType=content_type,
                                                            accept=accept,
                                                            modelId= model_id
                                                        )
        response_body = json.loads(response.get('body').read())
        #print(response_body)
        #print(type(references))
        return(response_body.get("outputs")[0]['text'])
    
    def get_response_from_bedrock_model_claude21(self,prompt):
        model_id= "anthropic.claude-v2:1"
    
        body = json.dumps({
                                    "prompt": f"""\n\nHuman: {prompt}"\n\nAssistant:""",
                                    "max_tokens_to_sample": max_tokens,
                                    "temperature": 0.1,
                                    "top_p": 0.9,
                                    
                                })
        response = self.bedrock_runtime.invoke_model(
                                                            body=body, #tab'bytes'|file,
                                                            contentType='application/json',
                                                            accept='application/json',
                                                            modelId= model_id
                                                        )
        response_body = json.loads(response.get('body').read())

        #print(response_body)
        #print(type(references))
        return(response_body['completion'])

    def get_bedrock_model_response(self, prompt, model):
        kb_response=self.get_knowledge_response_using_pagination(prompt)
        kb_text=kb_response['prompt']
        references=kb_response['location']
        
        prompt = f"""{prompt} using following 
            <text>
            {self.get_knowledgebase_response(prompt)}
            <text>
            """
        if model=="Llama2_13B":
            print(f"response from llama2 model!!!")
            response = self.get_response_from_bedrock_model_llama2(prompt)
        elif model=="Claude3-sonnet":
            print(f"response from claude3 model!!!")
            response = self.get_response_from_bedrock_model_claude3(prompt)
        else:
            print(f"response from claude3 model!!!")
            response = self.get_response_from_bedrock_model_claude3(prompt)
        response = {"response": response, 'location': references}
        return response
        
        
    def get_response_from_bedrock_model(self,prompt):
        
        kb_response=self.get_knowledge_response_using_pagination(prompt)
        kb_text=kb_response['prompt']
        references=kb_response['location']
        
        prompt = f"""{prompt} using following 
            <text>
            {self.get_knowledgebase_response(prompt)}
            <text>
            """
        """
        body = json.dumps(
                            {
                                "inputText":prompt,
                                "textGenerationConfig":{
                                    "maxTokenCount":256,
                                    "stopSequences":[],
                                    "temperature":0,
                                    "topP":1
                                }
                            }
                        )
        """
        body = json.dumps({
                                "prompt": f"""\n\nHuman: {prompt}"\n\nAssistant:""",
                                "max_tokens_to_sample": 4096,
                                "temperature": 0.1,
                                "top_p": 0.9,
                                
                            })
        response = self.bedrock_runtime.invoke_model(
                                                        body=body, #tab'bytes'|file,
                                                        contentType='application/json',
                                                        accept='application/json',
                                                        modelId=self.modelId
                                                    )
        response_body = json.loads(response.get('body').read())
        #print(response_body)
        #print(type(references))
        return(response_body['completion'], references)
