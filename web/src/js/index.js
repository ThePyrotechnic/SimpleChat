// simplechat - chat with AI
//     Copyright (C) 2024 Michael Manis - michaelmanis@tutanota.com
//     This program is free software: you can redistribute it and/or modify
//     it under the terms of the GNU Affero General Public License as published
//     by the Free Software Foundation, either version 3 of the License, or
//     (at your option) any later version.
//     This program is distributed in the hope that it will be useful,
//     but WITHOUT ANY WARRANTY; without even the implied warranty of
//     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
//     GNU Affero General Public License for more details.
//     You should have received a copy of the GNU Affero General Public License
//     along with this program.  If not, see <https://www.gnu.org/licenses/>.
const inputText = document.querySelector("#input-text");
const chatArea = document.querySelector("#div-chat-area");
const chatInputArea = document.querySelector("#chat-input-area");
const sendBtn = document.querySelector("#btn-send");
const tokenModal = document.querySelector("#token-modal");
const tokenBtn = document.querySelector("#btn-token");
const tokenInput = document.querySelector("#input-token");

const conversation = [];

const postChat = async () => {
  sendBtn.setAttribute("disabled", "");

  recordMessage("user", inputText.value)

  const response = await fetch("/api/converse", {
    method: "POST",
    body: JSON.stringify({
      "messages": conversation,
    }),
    headers: { "Content-Type": "application/json" }
  });

  console.assert(response.status === 200);

  const responseJson = await response.json();
  recordMessage(responseJson.role, responseJson.content[0].text.substring(2));
  sendBtn.removeAttribute("disabled");
};

const recordMessage = (role, text) => {
  conversation.push({"role": role, "content": [{"text": text}]},)

  const username = document.createElement("inline");
  username.classList.add(role);
  const message = document.createElement("p");
  message.classList.add(role)
  message.innerText = text;

  chatArea.appendChild(username);
  chatArea.appendChild(message);
};

const postToken = async () => {
  const tokenCheck = await fetch("/api/auth", {
    method: "POST",
    body: JSON.stringify({
      "api_key": tokenInput.value,
    }),
    headers: { "Content-Type": "application/json" }
  });

  if (tokenCheck.status === 200) {
    tokenModal.style.display = "none";
    chatInputArea.style.display = "flex";
  }
};

const authenticated = async () => {
  const authCheck = await fetch("/api/auth", {
      method: "HEAD",
    });

  return authCheck.status === 200;
};

document.addEventListener('DOMContentLoaded', async () => {
  if (await authenticated()) {
    // authed
  } else {
    tokenModal.style.display = "flex";
    chatInputArea.style.display = "none";
  }

  document.querySelector("#btn-send").addEventListener("click", postChat);
  document.querySelector("#btn-token").addEventListener("click", postToken);
});
