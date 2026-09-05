from fastapi import FastAPI, WebSocket
import base64
import diarization
import os
import llm

app = FastAPI()


@app.websocket("/chat")
async def chat(websocket: WebSocket):
    await websocket.accept()
    llm.reset_history()

    while True:
        data = await websocket.receive_text()
        decoded_data = base64.b64decode(data)
        with open("audio/input.wav", "wb") as f:
            f.write(decoded_data)
        file_location = os.path.join("audio", "input.wav")
        # audio_arr = np.frombuffer(decoded_data, dtype=np.int16)
        output_data = diarization.main(file_location)
        await websocket.send_text(output_data)


@app.get("/test")
def test():
    return "Hello"


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level="info")
