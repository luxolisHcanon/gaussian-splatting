from fastapi import FastAPI
from pydantic import BaseModel
from server_src.model_generation import generate_and_upload_3d_model_from_photos, generate_and_upload_3d_model_from_video

app = FastAPI(debug=True)


class ReconstructionRequest(BaseModel):
    s3_path: str


@app.post("/reconstruction/nerf/video")
async def create_and_upload_model(request: ReconstructionRequest):
    response = await generate_and_upload_3d_model_from_video(request.s3_path)

    return {"success": True if response < 400 else False, 'upload_response': response}


@app.post("/reconstruction/nerf/photos")
async def create_and_upload_model(request: ReconstructionRequest):
    response = await generate_and_upload_3d_model_from_photos(request.s3_path)

    return {"success": True if response < 400 else False, 'upload_response': response}
