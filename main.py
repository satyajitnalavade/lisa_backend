# uvicorn main:app
# uvicorn main:app --reload

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from decouple import config
import openai 
import uvicorn

# Custom Function Imports
from functions.database import store_messages, reset_messages
from functions.openai_requests import Convert_audio_to_text, get_chat_response
# from functions.text_to_speech import convert_text_to_speech
from functions.text_to_polly import convert_text_to_speech

# Initiate App
app = FastAPI()

# CORS - Origins
origins = [
    "http://localhost:5173",
    "http://localhost:5174",
    "http://localhost:4173",
    "http://localhost:4174",
    "http://localhost:3000",
    "https://your-frontend-domain.com",
]

# CORS - Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],

)


# check Health
@app.get("/health")
async def check_health():
    return {"message": "healthy"}

# Reset Messages
@app.get("/reset")
async def reset_conversation():
    reset_messages()
    return {"message": "conversation reset"}


# Get audio
# @app.get("/get-audio/")
# async def get_audio():
@app.post("/post-audio/")
async def post_audio(file: UploadFile = File(...)):

    # # Get saved audio
    # audio_input = open("voice.mp3", "rb")

    # Save file from Frontend
    with open(file.filename,"wb") as buffer:
        buffer.write(file.file.read())
    audio_input=open(file.filename, "rb")


    # Decode Audio
    message_decoded = Convert_audio_to_text(audio_input)

    # Guard: Ensure message decoded
    if not message_decoded:
        return HTTPException(status_code=400, detail="Fail to decode audio")
    
    # Get ChatGPT Response
    chat_response = get_chat_response(message_decoded)

    # Guard: Ensure message decoded
    if not chat_response:
        return HTTPException(status_code=400, detail="Fail to get chat response")

    # Store``==== messages
    store_messages(message_decoded, chat_response )

    # Convert chat response to audio
    audio_output = convert_text_to_speech(chat_response)

    # Guard: Ensure message decoded
    if not message_decoded:
        return HTTPException(status_code=400, detail="Failed to get Audio response")
                             
    # Create a generator that yields chunk of data
    def iterfile():
        yield audio_output

    # Return Audio file
    # return StreamingResponse(iterfile(), media_type="audio/mpeg")
    return StreamingResponse(iterfile(), media_type="application/octet-stream")

    #print(chat_response)

    if __name__ == "__main__":
    # Use uvicorn to run the app
    uvicorn.run(app, host="0.0.0.0", port=8000)