from fastapi import FastAPI
from pydantic import BaseModel
from server_src.model_generation import generate_and_upload_3d_model

app = FastAPI(debug=True)


class ReconstructionRequest(BaseModel):
    s3_path: str


@app.post("/nerf-reconstruction")
async def create_and_upload_model(request: ReconstructionRequest):
    s3_path = request.s3_path
    print("---STARTED API---")
    print(f"s3_path -> {s3_path}")
    response = await generate_and_upload_3d_model(s3_path)

    return {"success": True, 'upload_response': response}
