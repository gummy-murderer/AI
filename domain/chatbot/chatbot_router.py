from fastapi import APIRouter
from datetime import datetime
import requests
import json

from domain.chatbot.chatbot_schema import GeneratorSchema, ConversationUserSchema, ConversationNPCSchema
from LLMs.langchain import chatbot, prompts
# from lang_agency import chatbot, memory


router = APIRouter(
    prefix="/api/chatbot",
)

@router.get("/hello", tags=["hello"])
async def hello():
    return {"content": "Hello World!"}


@router.post("/intro_generator", tags=["conversation_with_user"])
async def intro_generator(generator_schema: GeneratorSchema):
    print(f"input : {generator_schema.content}")
    
    while True:
        try:
            answer = chatbot.intro(
                generator_schema.content
            )
            break
        except IndexError as e:
            print("#"*10 + "I got IndexError...Try again!" + "#"*10)

    final_response = {
        "answer": answer, 
    }
    print(f"answer : {answer}")
    return final_response


@router.post("/scenario_generator", tags=["conversation_with_user"])
async def scenario_generator(generator_schema: GeneratorSchema):
    print(f"input : {generator_schema.content}")
    
    while True:
        try:
            answer = chatbot.scenario(
                generator_schema.content
            )
            break
        except IndexError as e:
            print("#"*10 + "I got IndexError...Try again!" + "#"*10)

    final_response = {
        "answer": answer, 
    }
    print(f"answer : {answer}")
    return final_response


@router.post("/conversation_with_user", tags=["conversation_with_user"])
async def conversation_with_user(conversation_user_schema: ConversationUserSchema):
    print(f"input")
    print(f"sender : {conversation_user_schema.sender}")
    print(f"receiver : {conversation_user_schema.receiver}")
    print(f"chatContent : {conversation_user_schema.chatContent}")
    print(f"chatDay : {conversation_user_schema.chatDay}")
    
    while True:
        try:
            answer = chatbot.conversation_with_user(
                f" user: {conversation_user_schema.chatContent}" \
                + f" target_npc: {conversation_user_schema.receiver}" \
            )
            break
        except IndexError as e:
            print("#"*10 + "I got IndexError...Try again!" + "#"*10)

    final_response = {
        "answer": answer, 
    }
    print(f"answer : {answer}")
    return final_response


@router.post("/conversation_between_npcs", tags=["conversation_between_npcs"])
async def conversation_between_npc(conversation_npc_schema: ConversationNPCSchema):
    print(f"input")
    print(f"npc_name_1 : {conversation_npc_schema.npc_name_1}")
    print(f"npc_name_2 : {conversation_npc_schema.npc_name_2}")
    
    while True:
        try:
            answer = chatbot.conversation_between_npc(
                prompts.conversation_between_npc_prompt,
                conversation_npc_schema.npc_name_1,
                conversation_npc_schema.npc_name_2
            )
            break
        except IndexError as e:
            print("#"*10 + "I got IndexError...Try again!" + "#"*10)

    final_response = {
        "answer": answer, 
    }
    print(f"answer : {answer}")
    return final_response


@router.get("/make_npc", tags=["conversation_with_user"])
async def conversation_between_npc(npc_number: int):
    data = {
        "npcName": "testNpc1",
        "npcPersonality": "Friendly",
        "npcFeature": "Helpful and kind-hearted"
        }
    url = "http://221.140.195.124:9199/api/v1/npc/enroll"
    response = requests.post(url, json=data)
    
    result = json.loads(response.text)
    print(f'Status Code: {response.status_code}')
    print(f'Response Content : {json.dumps(result, indent=4)}')
    
    # Blend to fbx converter
    # if response.status_code == 200:
    #     BtoB_result = json.loads(response.text)
    #     blend_path = f"statics/blend_file/{BtoB_result['blend_name']}"
    #     size_multiplier = round(self.size / BtoB_result['size'], 1) if self.size else 1
        
    #     fbx_file_path = self.bpy_subprocess(blend_path, size_multiplier)
        

    #     print(f'convert successfully!   >> {fbx_file_path}')
    #     return fbx_file_path
    # else:
    #     print(f'make bled error : {preprocessing_result}')

    return npc_number