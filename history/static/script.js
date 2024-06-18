// Lấy ảnh từ history để hiện lên trang chủ 
document.addEventListener("DOMContentLoaded", function() {
  fetch('/images')
    .then(response => response.json())
    .then(images => {
      const imagelist = document.querySelector('.imagelist');
      images.forEach((image, index) => {
        const imgDiv = document.createElement('div');
        imgDiv.id = `khung-${index}`;
        imgDiv.classList.add('khung'); // Thêm class khung vào div

        const imgElement = document.createElement('img');
        imgElement.src = `/images/history/${image.filename}`;
        imgElement.alt = "Image";
        imgElement.classList.add('khung-img'); 
        imgDiv.appendChild(imgElement);
        
        const dateDiv = document.createElement('div');
        dateDiv.classList.add('date-container'); // Thêm class date-container vào div

        const dateLabel = document.createElement('h1');
        dateLabel.textContent = 'Ngày:';
        dateLabel.classList.add('date-label'); // Thêm class date-label vào h1

        const dateValue = document.createElement('p');
        dateValue.style.margin = '2px';
        dateValue.textContent = image.date;

        dateDiv.appendChild(dateLabel);
        dateDiv.appendChild(dateValue);

        imgDiv.appendChild(dateDiv);
        imagelist.appendChild(imgDiv);



        imgElement.addEventListener('click', function() {
          fetch('/find_image', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({ filename: image.filename })
          })
          .then(response => response.json())
          .then(data => {
            const resultSection = document.querySelector('.result');
            resultSection.innerHTML = ''; // Clear previous results
            if (data.found) {
              const resultImg = document.createElement('img');
              resultImg.src = data.path;
              resultImg.alt = "Result Image";
              resultImg.style.maxWidth = '100%';
              resultSection.appendChild(resultImg);
              resultSection.style.display = 'flex';
            } else {
              resultSection.innerHTML = '<p>Image not found in test folder</p>';
              resultSection.style.display = 'flex';
            }
          })
          .catch(error => console.error('Error finding image:', error));
        });
        
      });
    })
    .catch(error => console.error('Error fetching images:', error));
});

window.onload = fetchImages;
// ================================================================================================= // 


// click vào 1 khung sẽ mở kết quả
document.addEventListener('DOMContentLoaded', function() {
  document.getElementById('khung').addEventListener('click', function() {
      var resultSection = document.querySelector('.result');
      if (resultSection.style.display === 'none' || resultSection.style.display === '') {
          resultSection.style.display = 'flex';
      } else {
          resultSection.style.display = 'none';
      }
  });
});
// ================================================================================================= // 




