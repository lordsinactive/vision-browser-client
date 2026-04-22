from enum import StrEnum
from typing import Any, List, Optional

from pydantic import BaseModel


class OSType(StrEnum):
    MACOS = 'macos'
    WINDOWS = 'windows'
    LINUX = 'linux'


class SmartMode(StrEnum):
    STANDARD = 'standard'
    ENHANCED = 'enhanced'


class FingerprintScreen(BaseModel):
    width: int
    height: int
    pixel_ratio: float
    avail_width: int
    avail_height: int
    avail_top: int
    avail_left: int
    color_depth: int
    pixel_depth: int


class FingerprintHints(BaseModel):
    architecture: str
    bitness: int
    model: str
    platform: str
    platform_version: str
    ua_full_version: str
    mobile: bool


class FingerprintMediaDevices(BaseModel):
    audio_input: int
    audio_output: int
    video_input: int


class FingerprintNavigator(BaseModel):
    hardware_concurrency: int
    device_memory: float
    max_touch_points: int
    user_agent: str
    platform: str
    language: str
    languages: List[str]
    quota: int
    media_devices: Optional[FingerprintMediaDevices] = None


class FingerprintWebglExtra(BaseModel):
    uniform_buffer_offset_alignment: int
    max_elements_vertices: int
    max_elements_indices: int
    max_draw_buffers: int
    min_program_texel_offset: int
    max_program_texel_offset: int
    max_color_attachments: int
    max_vertex_texture_image_units: int
    max_texture_image_units: int
    max_3d_texture_size: int
    max_texture_lod_bias: int
    max_fragment_uniform_components: int
    max_vertex_uniform_components: int
    max_array_texture_layers: int
    max_varying_components: int
    max_transform_feedback_separate_components: int
    max_transform_feedback_interleaved_components: int
    max_samples: int
    max_vertex_uniform_blocks: int
    max_fragment_uniform_blocks: int
    max_combined_uniform_blocks: int
    max_uniform_buffer_bindings: int
    max_uniform_block_size: int
    max_combined_vertex_uniform_components: int
    max_combined_fragment_uniform_components: int
    max_vertex_output_components: int
    max_fragment_input_components: int
    max_element_index: float
    max_texture_size: int
    max_vertex_attribs: int
    max_vertex_uniform_vectors: int
    max_varying_vectors: int
    max_combined_texture_image_units: int
    max_fragment_uniform_vectors: int
    max_cube_map_texture_size: int
    max_renderbuffer_size: int
    max_viewport_width: int
    max_viewport_height: int
    aliased_line_width_range_min: float
    aliased_line_width_range_max: float
    aliased_point_size_range_min: float
    aliased_point_size_range_max: float
    max_server_wait_timeout: Optional[int] = None


class FingerprintWebgl(BaseModel):
    unmasked_renderer: str
    unmasked_vendor: str
    extensions: List[str]
    extensions_v2: List[str]
    extra: FingerprintWebglExtra


class FingerprintWebgpuLimits(BaseModel):
    maxBindGroups: int
    maxBindGroupsPlusVertexBuffers: Optional[int] = None
    maxBindingsPerBindGroup: int
    maxBufferSize: float
    maxColorAttachmentBytesPerSample: Optional[int] = None
    maxColorAttachments: int
    maxComputeInvocationsPerWorkgroup: int
    maxComputeWorkgroupSizeX: int
    maxComputeWorkgroupSizeY: int
    maxComputeWorkgroupSizeZ: int
    maxComputeWorkgroupStorageSize: int
    maxComputeWorkgroupsPerDimension: int
    maxDynamicStorageBuffersPerPipelineLayout: int
    maxDynamicUniformBuffersPerPipelineLayout: int
    maxImmediateSize: Optional[int] = None
    maxInterStageShaderComponents: Optional[int] = None
    maxInterStageShaderVariables: int
    maxSampledTexturesPerShaderStage: int
    maxSamplersPerShaderStage: int
    maxStorageBufferBindingSize: Optional[int] = None
    maxStorageBuffersInFragmentStage: Optional[int] = None
    maxStorageBuffersInVertexStage: Optional[int] = None
    maxStorageBuffersPerShaderStage: int
    maxStorageTexturesInFragmentStage: Optional[int] = None
    maxStorageTexturesInVertexStage: Optional[int] = None
    maxStorageTexturesPerShaderStage: int
    maxTextureArrayLayers: int
    maxTextureDimension1D: int
    maxTextureDimension2D: int
    maxTextureDimension3D: int
    maxUniformBufferBindingSize: int
    maxUniformBuffersPerShaderStage: int
    maxVertexAttributes: int
    maxVertexBufferArrayStride: int
    maxVertexBuffers: int
    minStorageBufferOffsetAlignment: int
    minUniformBufferOffsetAlignment: int


class FingerprintWebgpu(BaseModel):
    vendor: str
    architecture: str
    features: Optional[List[str]] = None
    limits: FingerprintWebgpuLimits
    subgroupMinSize: Optional[int] = None
    subgroupMaxSize: Optional[int] = None


class FingerprintOptions(BaseModel):
    args: Optional[List[str]] = None


class Fingerprint(BaseModel):
    major: int
    os: OSType
    screen: FingerprintScreen
    fonts: List[str]
    hints: FingerprintHints
    navigator: FingerprintNavigator
    webgl: FingerprintWebgl
    webgpu: Optional[FingerprintWebgpu] = None
    crc: str
    webrtc_pref: Optional[str | dict[str, Any]] = None
    webgl_pref: Optional[str | dict[str, Any]] = None
    canvas_pref: Optional[str | dict[str, Any]] = None
    audio_pref: Optional[float] = None
    client_rects: Optional[float] = None
    ports_protection: Optional[List[int]] = None
    geolocation: Optional[dict[str, Any]] = None
    media_devices: Optional[FingerprintMediaDevices | dict[str, Any]] = None
    options: Optional[FingerprintOptions | dict[str, Any]] = None