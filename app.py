import os
from fastapi import FastAPI, File, UploadFile
from uvicorn import run
import amfm_decompy.pYAAPT as pYAAPT
import amfm_decompy.basic_tools as basic

app = FastAPI()
@app.post("/upload_audio/")
async def root(audio: UploadFile = File(...)):
    print(audio.file)
    try:
        os.mkdir("testing")
        print(os.getcwd())
    except Exception as e:
        print(e)
    filedir = os.getcwd()+"/testing/"+audio.filename.replace(" ", "-")
    file_name= os.path.basename(filedir)

    with open(os.getcwd()+"/testing/"+file_name,'wb') as f:
        f.write(audio.file.read())
        f.close()

    print(file_name)

    path = f"{filedir}"
    signal = basic.SignalObj(path)
    pitch = pYAAPT.yaapt(signal)
    pitch_value = pitch.samp_values
    print(pitch_value)
    value = ["".join(item) for item in pitch_value.astype(str)]
    # print(value)
    return {"filename": file_name, " pitch": value}


if __name__ == "__main__":
    run(app, host="0.0.0.0", port=7000)