document.addEventListener('DOMContentLoaded', function() {
  const toggleButton = document.getElementById('toggle-button');
  const khungElements = document.querySelectorAll('.container .khung');
  let showingAll = false;

  function updateKhungDisplay() {
      khungElements.forEach((khung, index) => {
          if (showingAll) {
              khung.style.display = 'block';
          } else {
              khung.style.display = index < 6 ? 'block' : 'none';
          }
      });
      toggleButton.textContent = showingAll ? 'Ẩn bớt' : 'Hiển thị thêm';
  }

  toggleButton.addEventListener('click', function() {
      showingAll = !showingAll;
      updateKhungDisplay();
  });

  // Initialize display
  updateKhungDisplay();

  // Existing code for overlay and content
  const acneImg = document.querySelector('img[alt="acne"]');
  const acneContent = document.getElementById('acne-content');
  const overlay = document.getElementById('overlay');
  const content = document.getElementById('content');
  const closeButton = document.getElementById('close');

  acneImg.addEventListener('click', function() {
      fetch('../templates/acne.html')
          .then(response => response.text())
          .then(data => {
              acneContent.innerHTML = data;
              content.style.display = 'block';
              overlay.style.display = 'block';
          })
          .catch(error => console.error('Error fetching content:', error));
  });

  overlay.addEventListener('click', function() {
      content.style.display = 'none';
      overlay.style.display = 'none';
  });

  closeButton.addEventListener('click', function() {
      content.style.display = 'none';
      overlay.style.display = 'none';
  });
});


document.addEventListener('DOMContentLoaded', function() {
  const overlay = document.getElementById('overlay');
  const content = document.getElementById('content');
  const closeButton = document.getElementById('close');
  const khungImages = document.querySelectorAll('.khung-img');

  khungImages.forEach(img => {
    img.addEventListener('click', function() {
      const diseaseType = img.alt;
      fetch(`/templates/${diseaseType}.html`)
        .then(response => response.text())
        .then(data => {
          document.getElementById('body').innerHTML = data; 
          content.style.display = 'block';
          overlay.style.display = 'block';
        })
        .catch(error => console.error('Error fetching content:', error));
    });
  });

  overlay.addEventListener('click', function() {
    content.style.display = 'none';
    overlay.style.display = 'none';
  });

  closeButton.addEventListener('click', function() {
    content.style.display = 'none';
    overlay.style.display = 'none';
  });
});


// Chat box
document.addEventListener("DOMContentLoaded", function () {
  const chatCircle = document.getElementById("chat-icon");
  const chatBox = document.getElementById("chat-box");
  const closeButton = document.getElementById("close-button");
  const chatContent = document.getElementById("chat-content");
  const userInput = document.getElementById("user-input");
  const sendButton = document.getElementById("send-button");

  let isOpen = false;

  function toggleChatBox() {
    isOpen = !isOpen;
    chatBox.style.display = isOpen ? "block" : "none";
    overlay.style.display = isOpen ? "block" : "none";
  }

  overlay.addEventListener('click', function() {
    content.style.display = 'none';
    overlay.style.display = 'none';
  });

  closeButton.addEventListener('click', function() {
    content.style.display = 'none';
    overlay.style.display = 'none';
  });

  function closeChatBox() {
    isOpen = false;
    chatBox.style.display = "none";
    overlay.style.display = 'none';
  }

  function appendMessage(sender, message, isTitle = false) {
    const messageElement = document.createElement("div");

    // Split the message by new lines and add <br/> tags
    const messageParts = message.split("\n");
    const formattedMessage = messageParts.join("<br/>");

    if (isTitle) {
      messageElement.innerHTML = `<strong style="color: #e9a084">${sender}:</strong><br/>${message}`;
    } else {
      // Append a line break at the end of the formatted message
      messageElement.innerHTML = `<strong>${sender}:</strong> ${formattedMessage}<br/>`;
    }

    chatContent.appendChild(messageElement);
    chatContent.scrollTop = chatContent.scrollHeight;
  }

  function sendMessage() {
    const userMessage = userInput.value.trim();
    if (userMessage !== "") {
      // Thay vì sử dụng formattedUserMessage, hãy truyền userMessage trực tiếp
      appendMessage("Bạn", userMessage);

      // Call your backend API to get the bot's response
      // Example: You can use the Fetch API or an AJAX library
      // Replace the URL with your actual backend endpoint
      let xhr = new XMLHttpRequest();
      xhr.open("POST", "/askGPT");
      xhr.setRequestHeader("Accept", "application/json");
      xhr.setRequestHeader("Content-Type", "application/json");

      xhr.onreadystatechange = function () {
        if (xhr.readyState === 4) {
          console.log(xhr.status);
          // console.log(xhr.responseText);

          // Append chatbot's response with a line break
          appendMessage("Tư vấn", JSON.parse(xhr.responseText).content + "\n");
        }
      };

      xhr.send(JSON.stringify({ message: userMessage }));

      userInput.value = "";
    }
  }

  chatCircle.addEventListener("click", toggleChatBox);
  closeButton.addEventListener("click", closeChatBox);
  sendButton.addEventListener("click", sendMessage);
  userInput.addEventListener("keyup", function (event) {
    if (event.key === "Enter") {
      sendMessage();
    }
  });
});
