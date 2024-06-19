from dataclasses import dataclass
from io import BytesIO
from typing import Any

from openai.types.audio.transcription import Transcription
from pyannote.audio import Pipeline
from pyannote.audio.core.inference import torch
from pyannote.core import Segment
from pyannote.core.annotation import Label
from pyannote.pipeline.pipeline import Annotation

from f_api import config as cfg


@dataclass
class TextSegment:
    segment: Segment
    text: str
    speaker: Label

def build_text_segments(
    whisper_segments: list[dict[str, Any]],
    annotation: Annotation,
) -> list[TextSegment]:
    segments = []
    for whisper_segment in whisper_segments:
        segment = Segment(
            start=whisper_segment["start"],
            end=whisper_segment["end"]
        )

        speaker = annotation.crop(segment).argmax()
        if not speaker:
            speaker = "Unknown"

        text_segment = TextSegment(
            segment=segment,
            text=whisper_segment["text"],
            speaker=speaker,
        )

        segments.append(text_segment)

    return segments

def format_segments_to_text(segments: list[TextSegment]) -> str:
    lines = []
    for segment in segments:
        lines.append(f"{segment.speaker}: {segment.text}")

    return "\n".join(lines)

def build_diarization_pipeline() -> Pipeline:
    pipeline = Pipeline.from_pretrained(
        cfg.DIARIZATION_MODEL,
        use_auth_token=cfg.HUGGINGFACE_TOKEN,
    )
    pipeline.to(torch.device(cfg.TORCH_DEVICE))
    return pipeline

def diarize_audio(
    audio_bytes: BytesIO,
    transcription: Transcription,
) -> str:
    diarization_pipeline = build_diarization_pipeline()
    annotation  = diarization_pipeline(audio_bytes)
    print(annotation)

    segments = build_text_segments(
        whisper_segments=transcription.segments,
        annotation=annotation,
    )
    print(segments)
    return format_segments_to_text(segments)
