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

from functools import lru_cache
import os

from pydantic_settings import BaseSettings, SettingsConfigDict


@lru_cache
def settings():
    return _Settings()


class _Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=os.environ.get("SIMPLECHAT_ENV_FILE"), env_file_encoding="utf-8"
    )

    aws_profile: str | None = None
    aws_region: str
    bedrock_model_id: str
    host: str
    hot_reload: bool = False
    port: int
    private_key_filepath: str
    public_key_filepath: str
