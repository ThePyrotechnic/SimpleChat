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

from fastapi.testclient import TestClient
import pytest

from simplechat import app


@pytest.fixture(scope="module")
def authed_client():
    client = TestClient(app)
    client.get("/token")
    return client


def test_new_chat(authed_client):
    response = authed_client.post(
        "/converse",
        json={"messages": [{"role": "user", "content": [{"text": "Who are you?"}]}]},
    )

    assert response.status_code == 200
    assert response.json()["role"] == "assistant"


def test_chat_replies(authed_client):
    question_1 = {"role": "user", "content": [{"text": "Who are you?"}]}
    response_1 = authed_client.post(
        "/converse",
        json={"messages": [question_1]},
    )

    assistant_answer_1 = response_1.json()

    question_2 = {
        "role": "user",
        "content": [{"text": "What question did I just ask you?"}],
    }
    response_2 = authed_client.post(
        "/converse",
        json={"messages": [question_1, assistant_answer_1, question_2]},
    )
    assert response_2.status_code == 200
    assert response_2.json()["role"] == "assistant"
