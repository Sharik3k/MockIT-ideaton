from pydantic import BaseModel

class ResumeResponse(BaseModel):
    id: str
    candidateId: str
    workspaceId: str
    originalFilename: str
    storedFilename: str
    filePath: str
    mimeType: str
    fileSize: int
    uploadedAt: str
