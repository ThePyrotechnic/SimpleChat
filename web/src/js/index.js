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

const accessToken = document.cookie.split("; ")
  .find((row) => row.startsWith("access_token="))?.split("=")[1];

const inputText = document.querySelector("#input-text");
const chatArea = document.querySelector("#div-chat-area");
const sendBtn = document.querySelector("#btn-send");

const conversation = [];

const onWindowResize = () => {
  const width = window.innerWidth;
  const height = window.innerHeight;
};

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

const authenticated = () => {
  return accessToken != null;
};

const logout = () => {
  document.cookie = "access_token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
  window.location.reload();
};

document.addEventListener('DOMContentLoaded', async () => {
  if (authenticated()) {
    // authed
  } else {
    await fetch("/api/token", {
      method: "GET",
      headers: { "Content-Type": "application/json" }
    });
  }

  document.querySelector("#btn-send").addEventListener("click", postChat);

  window.addEventListener("resize", onWindowResize);
});
