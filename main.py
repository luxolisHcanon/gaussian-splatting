from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(debug=True)


class ReconstructionRequest(BaseModel):
    url: str
    upload_url: str


@app.post("/nerf-reconstruction")
async def create_upload_file(request: ReconstructionRequest):
    download_url = request.url
    upload_url = request.upload_url
    print("STARTED API")
    print(f"download url -> {download_url}")
    print(f"upload url -> {upload_url}")
    # upload_response = await convert_usdz_upload_glb(download_url, upload_url)

    return {"success": True, 'upload_response': 200}
