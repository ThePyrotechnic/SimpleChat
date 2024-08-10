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
let inputText;
let chatArea;
let chatInputArea;
let sendBtn;
let tokenModal;
let tokenBtn;
let tokenInput;

const conversation = [];

const postChat = async () => {
  sendBtn.setAttribute("disabled", "");

  recordMessage("user", inputText.value)
  inputText.value = "";

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
  const message = document.createElement("div");

  let messageClasses;
  if (role === "user") {
    username.innerText = "You";
    messageClasses = ["mx-2", "self-end", "bg-send-bg", "text-send-text", "rounded-lg", "px-4", "py-2"];
  } else {
    username.innerText = "AI";
    messageClasses = ["px-8", "py-2", "mx-2", "bg-receive-bg", "rounded-lg", "text-receive-text"];
  }

  message.classList.add(...messageClasses);
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

  tokenInput.value = "";

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

const onEnterPressed = async (btn, e) => {
  if (e.key !== "Enter") return;

  btn.dispatchEvent(new Event("click", { bubbles: true }));
}

document.addEventListener('DOMContentLoaded', async () => {
  inputText = document.querySelector("#input-text");
  chatArea = document.querySelector("#chat-area");
  chatInputArea = document.querySelector("#chat-input-area");
  sendBtn = document.querySelector("#btn-send");
  tokenModal = document.querySelector("#token-modal");
  tokenBtn = document.querySelector("#btn-token");
  tokenInput = document.querySelector("#input-token");
  
  if (await authenticated()) {
    tokenModal.style.display = "none";
  } else {
    tokenModal.style.display = "flex";
    chatInputArea.style.display = "none";
  }
  tokenBtn.addEventListener("click", postToken);
  sendBtn.addEventListener("click", postChat);
  inputText.addEventListener("keydown", async (e) => { await onEnterPressed(sendBtn, e) });
  tokenInput.addEventListener("keydown", async (e) => { await onEnterPressed(tokenBtn, e) });
  inputText.focus();
});
