from fastapi import FastAPI
from pydantic import BaseModel
from server_src.services.api import post_request
from server_src.model_generation import (generate_and_upload_3d_model_from_photos,
                                         generate_and_upload_3d_model_from_video)

app = FastAPI(debug=True)


class ReconstructionRequestWithCallback(BaseModel):
    s3_path: str
    file_info: object
    cad_file_id: int
    model_name: str
    x_access_token: str
    callback_url: str


class ReconstructionRequest(BaseModel):
    s3_path: str


@app.post("/reconstruction/nerf/video")
async def create_and_upload_model(request: ReconstructionRequestWithCallback):
    response = 200 # await generate_and_upload_3d_model_from_video(request.s3_path)
    if response >= 400:
        return {'success': False, 'upload_response': response}

    callback_payload = {
        'fileInfo': request.file_info,
        'cadFileId': request.cad_file_id,
        'modelName': request.model_name
    }
    post_request(request.callback_url, callback_payload, request.x_access_token)

    return {"success": True, 'upload_response': response}


@app.post("/reconstruction/nerf/photos")
async def create_and_upload_model(request: ReconstructionRequest):
    response = await generate_and_upload_3d_model_from_photos(request.s3_path)

    return {"success": True if response < 400 else False, 'upload_response': response}
