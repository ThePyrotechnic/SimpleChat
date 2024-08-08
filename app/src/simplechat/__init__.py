"""
simplechat - chat with AI
    Copyright (C) 2024 Michael Manis - michaelmanis@tutanota.com
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published
    by the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.
    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import json

import boto3
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicKey
from fastapi import Depends, FastAPI, HTTPException, Security, status
from fastapi.responses import JSONResponse, Response
from fastapi.security import APIKeyCookie
import jwt

from simplechat.models import ConversationInput, Message, TokenInput
from simplechat.settings import settings


api_key_cookie = APIKeyCookie(name="access_token", auto_error=True)


app = FastAPI(title="SimpleChat API", description="", version="0.1.0")


bedrock = boto3.Session(
    profile_name=settings().aws_profile, region_name=settings().aws_region
).client("bedrock-runtime")


with open(settings().public_key_filepath, "rb") as public_key_file:
    PUBLIC_KEY: RSAPublicKey = serialization.load_pem_public_key(public_key_file.read())


with open(settings().tokens_filepath, "r", encoding="UTF-8") as tokens_file:
    TOKENS = json.load(tokens_file)


async def check_api_key(api_key: str = Security(api_key_cookie)) -> str:
    try:
        token = jwt.decode(api_key, PUBLIC_KEY, ["RS256"])
    except jwt.DecodeError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    try:
        TOKENS[token["claimed_id"]]
    except KeyError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    return token


@app.get("/summary/today", tags=["summary"])
async def get_daily_summary(_=Depends(check_api_key)):
    return JSONResponse({"summary": "this is the summary"})


@app.post("/converse", tags=["chat"])
async def post_conversation(
    conversation: ConversationInput, _=Depends(check_api_key)
) -> Message:
    response = bedrock.converse(
        modelId=settings().bedrock_model_id,
        messages=conversation.model_dump()["messages"],
        inferenceConfig={
            "temperature": 0.5,
            "topP": 0.9,
            "maxTokens": 512,
        },
    )
    return Message(
        role=response["output"]["message"]["role"],
        content=response["output"]["message"]["content"],
    )


@app.head("/auth", tags=["auth"])
async def check_token(_=Depends(check_api_key)):
    return


@app.post("/auth", tags=["auth"])
async def post_token(token_input: TokenInput):
    await check_api_key(token_input.api_key)

    response = Response(status_code=status.HTTP_200_OK)
    response.set_cookie(
        key="access_token",
        value=token_input.api_key,
        expires=60 * 60 * 24 * 30,  # 1 month
        secure=True,
        httponly=True,
        samesite="strict",
    )
    return response
