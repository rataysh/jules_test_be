from pydantic import BaseModel, Field
from typing import List, Optional

class NewsRequest(BaseModel):
    twitter_links: Optional[List[str]] = Field(
        default=[
            "https://x.com/OpenAI?t=QDW1TzDcECG9Bq45Q55EZg&s=09",
            "https://x.com/AnthropicAI?t=N5MbfPVV0iHl2D0qweHbCg&s=09",
            "https://x.com/cursor_ai?t=WiciRO5CQzT5Z_w5x0uC5w&s=09",
            "https://x.com/ilyasut?t=_1gep75ZtdIbnIHEZdXujw&s=09",
            "https://x.com/karpathy?t=9cRAMtUvhVKaVkUMzuL0qw&s=09",
            "https://x.com/ylecun?t=oxOD6mcEgOcIS1fbifx-nw&s=09",
            "https://x.com/DarioAmodei?t=44fpuLBSOWq1TVZICnLSWw&s=09",
            "https://x.com/xai?t=Hd3427DpeNHJrLIsNSYyhw&s=09",
            "https://x.com/deepseek_ai?t=gqhxrohZfJwDbxkTFfPvog&s=09",
            "https://x.com/MistralAI?t=2CmKkNAP_6-qYh-NHOki0g&s=09",
            "https://x.com/huggingface?t=ilo3U7EUR4k4hrGr864L8Q&s=09",
            "https://x.com/AIatMeta?t=qmAs4f-UysTtzegGTMjvow&s=09",
            "https://x.com/GoogleAI?t=NrVXgvcBXFepKWh-AYGr6w&s=09",
            "https://x.com/finkd?t=8_e7wZdzSfKIQdoIFYOX2w&s=09",
            "https://x.com/GeminiApp?t=60D_TY5bz7uN1-Mtc1FaRw&s=09",
            "https://x.com/GoogleDeepMind?t=RAr9G5rjohEZduX1dpkfjw&s=09",
            "https://x.com/satyanadella?t=3IRfim6FmrmKehRDZzeqdQ&s=09",
            "https://x.com/gdb?t=SzplTT5Gl1X8l0DfZ3Pw8g&s=09",
            "https://x.com/elonmusk?t=nLwHZSVW_1iK77zMu-T35w&s=09",
            "https://x.com/sama?t=XjqZUzbTEYgqTquLdJjisg&s=09",
        ]
    )
    days: int = Field(default=3, ge=1)
    language: str = Field(default="Russian")
