import sentivi
from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
from sentivi import Pipeline


class ResponseModel(BaseModel):
    polarity: str
    label: str

    class Config:
        schema_extra = {
            'example': [
                {
                    'polarity': 0,
                    'label': '#NEG',
                },
                {
                    'polarity': 1,
                    'label': '#NEU',
                },
                {
                    'polarity': 2,
                    'label': '#POS'
                }
            ]
        }


class RESTServiceGateway:
    server = FastAPI(
        title='Sentivi Web Services',
        description='A simple tool for sentiment analysis',
        version=sentivi.__version__
    )

    tags_metadata = [
        {
            'name': 'Predictor',
            'description': 'Sentiment Predictor'
        }
    ]

    response_models = {
        'foo': {
            'polarity': 'Numeric polarity',
            'label': 'Label from piplines\' label set'
        }
    }

    def __init__(self, pipeline: Optional[Pipeline], port: Optional[int], *args, **kwargs):
        super(RESTServiceGateway, self).__init__(*args, **kwargs)

        self.pipeline = pipeline
        self.port = port
        print('Initialized REST Service Gateway')

    @staticmethod
    @server.get('/get_sentiment/', tags=['Predictor'], response_model=ResponseModel)
    async def get_sentiment(text: str):
        print(text)

    @staticmethod
    def get_server():
        return RESTServiceGateway.server
