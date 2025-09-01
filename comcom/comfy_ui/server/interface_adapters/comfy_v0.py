from comcom.comfy_ui.models.raw.node_definitions.version_1_0.node_definitions import Comfy_v1_0_NodeDefinitions
from comcom.comfy_ui.server.models.comfyui_v0.image_upload import ComfyUI_v0_ImageUploadRequestModel
from comcom.comfy_ui.server.models.comfyui_v0.image_upload import ComfyUI_v0_ImageUploadResponseModel
from comcom.comfy_ui.server.models.comfyui_v0.image_upload import ComfyUI_v0_ImageUploadErrorResponseModel
from comcom.comfy_ui.server.models.comfyui_v0.prompt_history import ComfyUI_v0_PromptHistoryRequestModel
from comcom.comfy_ui.server.models.comfyui_v0.prompt_history import ComfyUI_v0_PromptHistoryResponseModel
from comcom.comfy_ui.server.models.comfyui_v0.submit_prompt import ComfyUI_v0_SubmitPromptRequestModel
from comcom.comfy_ui.server.models.comfyui_v0.submit_prompt import ComfyUI_v0_SubmitPromptResponseModel
from comcom.comfy_ui.server.models.comfyui_v0.submit_prompt import ComfyUI_v0_SubmitPromptErrorResponseModel

class ComfyUI_v0_InterfaceProvider:
    RawNodeDefinitionsModel = Comfy_v1_0_NodeDefinitions
    
    # Image Upload
    ImageUploadRequestModel = ComfyUI_v0_ImageUploadRequestModel
    ImageUploadResponseModel = ComfyUI_v0_ImageUploadResponseModel
    ImageUPloadErrorResponseModel = ComfyUI_v0_ImageUploadErrorResponseModel

    # Prompt History
    PromptHistoryRequestModel = ComfyUI_v0_PromptHistoryRequestModel
    PromptHistoryResponseModel = ComfyUI_v0_PromptHistoryResponseModel

    # Submit prompt
    SubmitPromptRequestModel = ComfyUI_v0_SubmitPromptRequestModel
    SubmitPromptResponseModel = ComfyUI_v0_SubmitPromptResponseModel
    SubmitPromptErrorResponseModel = ComfyUI_v0_SubmitPromptErrorResponseModel