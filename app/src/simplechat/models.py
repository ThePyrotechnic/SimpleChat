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

from typing_extensions import Literal

from pydantic import BaseModel


class ContentBlock(BaseModel):
    text: str


class Message(BaseModel):
    role: Literal["user", "assistant"]
    content: list[ContentBlock]


class ConversationInput(BaseModel):
    messages: list[Message]


class TokenInput(BaseModel):
    api_key: str
