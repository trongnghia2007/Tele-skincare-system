document.addEventListener("DOMContentLoaded", function() {
  fetch('/images')
    .then(response => response.json())
    .then(images => {
      const imagelist = document.querySelector('.imagelist');
      const resultlist = document.querySelector('.resultlist');

      let resultIndex = 0;

      images.forEach((image, index) => {
        if (image.folder === 'history') {
          // Thêm ảnh vào imagelist
          const imgDiv = document.createElement('div');
          imgDiv.id = `khung-${index}`;
          imgDiv.classList.add('khung');

          const imgElement = document.createElement('img');
          imgElement.src = image.path;
          imgElement.alt = "Image";
          imgElement.classList.add('khung-img');
          imgDiv.appendChild(imgElement);

          const dateDiv = document.createElement('div');
          dateDiv.classList.add('date-container');

          const dateLabel = document.createElement('h1');
          dateLabel.textContent = 'Ngày:';
          dateLabel.classList.add('date-label');

          const dateValue = document.createElement('p');
          dateValue.style.margin = '2px';
          dateValue.textContent = image.date;

          dateDiv.appendChild(dateLabel);
          dateDiv.appendChild(dateValue);

          imgDiv.appendChild(dateDiv);
          imagelist.appendChild(imgDiv);

          imgDiv.addEventListener('click', function() {
            const resultDiv = document.getElementById(`result-${index}`);
            if (resultDiv.style.display === 'none' || resultDiv.style.display === '') {
              resultDiv.style.display = 'flex';
            } else {
              resultDiv.style.display = 'none';
            }
          });
        } 

 // ======================================================================================================= //
        

        else if (image.folder === 'test') {
          // Thêm ảnh vào resultlist với display=none
          const resultDiv = document.createElement('div');
          resultDiv.id = `result-${resultIndex}`;
          resultDiv.classList.add('result');
          resultlist.appendChild(resultDiv);

          const frameDiv = document.createElement('div');
          frameDiv.classList.add('frame');
          resultDiv.appendChild(frameDiv);

          const resultImg = document.createElement('img');
          resultImg.src = image.path;
          resultImg.alt = "Result Image";
          resultImg.classList.add('frame-img');
          frameDiv.appendChild(resultImg);
          
          resultDiv.style.display = 'none';

          resultIndex++;
        } 
        
        else if (image.folder === 'segments') {
          const segmentIndex = parseInt(image.subfolder, 10);
          let resultDiv = document.getElementById(`result-${segmentIndex - 1}`);

          if (!resultDiv) {
            resultDiv = document.createElement('div');
            resultDiv.id = `result-${segmentIndex}`;
            resultDiv.classList.add('result');
            resultlist.appendChild(resultDiv);
          }

          const frameDiv = document.createElement('div');
          frameDiv.classList.add('frame-sm');
          resultDiv.appendChild(frameDiv);

          const resultImg = document.createElement('img');
          resultImg.src = image.path;
          resultImg.alt = "Segment Image";
          resultImg.classList.add('frame-sm-img');
          frameDiv.appendChild(resultImg);

          const description = document.createElement('p');
          description.textContent = image.filename.split('-')[1];
          description.textContent = description.textContent.split('.')[0];
          frameDiv.appendChild(description);

          resultDiv.style.display = 'none';
        }
      });
    })
    
    .catch(error => console.error('Error fetching images:', error));
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