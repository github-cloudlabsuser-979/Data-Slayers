import os 
from dotenv import load_dotenv
import asyncio
# Add Azure OpenAI Package
# from openai import AzureOpenAI
from openai import AsyncAzureOpenAI

printFullResponse=False
async def main():
    try:
        # Get Configuration Setting
        load_dotenv()
        azure_oai_endpoint=os.getenv("AZURE_OAI_ENDPOINT")
        azure_oai_key=os.getenv("AZURE_OAI_KEY")
        azure_oai_deployment=os.getenv("AZURE_OAI_DEPLOYMENT")
        azure_search_endpoint=os.getenv("AZURE_SEARCH_ENGINE_ENDPOINT")
        azure_search_key=os.getenv("AZURE_SEARCH_KEY")
        azure_search_index=os.getenv("AZURE_SEARCH_INDEX")
        # Configure the Azure OpenAI Client
        client=AzureOpenAI(
            base_url=f"{azure_oai_endpoint}/openai/deployments/{azure_oai_deployment}/extensions",
            api_key=azure_oai_key,
            api_version="2024-02-15-preview"
        )
        # system_message=input("Enter System Message..")

        # Initialize Messages Array
        # messages_array = [{"role": "system", "content": system_message}]

        while True:
            print("Press anything then enter to continue...")
            input()
            
            # Read the system message
            system_text=open(file='system.txt',encoding='utf8').read().strip()
            user_text=input("Enter the Prompt (or type 'quit' to exit)")
            if user_text.lower()=="quit" or system_text.lower()=='quit':
                print("Exiting the Program...")
                break
            extension_config = dict(dataSources = [  
                                { 
                                    "type": "AzureCognitiveSearch", 
                                    "parameters": { 
                                        "endpoint":azure_search_endpoint, 
                                        "key": azure_search_key, 
                                        "indexName": azure_search_index,
                                    }
                                }]
                            )

            await call_openai_model(
                system_message=system_text,
                user_message=user_text,
                model=azure_oai_deployment,
                client=client,
                extension_config=extension_config
            )
            # if len(input_text)==0:
            #     print("Please Enter a Prompt.")
            #     continue
            
            # print("\n Sending request for Summary to Azure OpenAI Endpoint...")
            
            # messages_array.append({"role":"user","content":input_text})
            # # Add code to send request
            # response=client.chat.completions.create(
            #     model=azure_oai_deployment,
            #     temperature=0.7,
            #     max_tokens=400,
            #     messages=messages_array
            # )
            # generated_text=response.choices[0].message.content

            # # Add generated text to messages array 
            # messages_array.append({"role":"system","content":generated_text})

            # # Print the Response
            # print("Response: "+generated_text+"\n")
    except Exception as ex:
        print(ex)

async def call_openai_model(system_message,user_message,model,client):
    messages=[
        {"role":"system","content":system_message},
        {"role":"user","content":user_message}
    ]

    print("\nSending request to Azure OpenAI Model...")
    response=await client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.7,
        max_tokens=800,
        extra_body=extension_config
    )
    if printFullResponse:
        print(response)
    
    print("Response:\n"+response.choices[0].messages.content+"\n")

 print("Response:\n" + response.choices[0].message.content + "\n")

if __name__=="__main__":
    asyncio.run(main())
    #main()
