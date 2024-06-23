document.addEventListener("DOMContentLoaded", function() {
  fetch('/images')
    .then(response => response.json())
    .then(images => {
      const imagelist = document.querySelector('.imagelist');
      const result = document.querySelector('.result');

      images.forEach((image, index) => {
        if (image.folder === 'history') {
          // Thêm ảnh vào imagelist
          const imgDiv = document.createElement('div');
          imgDiv.id = `khung-${index}`;
          imgDiv.classList.add('khung');

          const imgElement = document.createElement('img');
          imgElement.src = `/images/history/${image.filename}`;
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

          imgElement.addEventListener('click', function() {
            const resultImg = document.querySelector(`img[data-filename="${image.filename}"]`);
            if (resultImg) {
              if (resultImg.style.display === 'none' || resultImg.style.display === '') {
                resultImg.style.display = 'block';
              } else {
                resultImg.style.display = 'none';
              }
            }
          });
        } 
        
        else if (image.folder === 'test') {
          // Thêm ảnh vào result với display=none
          const resultImg = document.createElement('img');
          resultImg.src = `/images/test/${image.filename}`;
          resultImg.alt = "Result Image";
          resultImg.style.display = 'none';
          resultImg.dataset.filename = image.filename;  // Lưu trữ tên file để dễ truy cập
          result.appendChild(resultImg);
        }
      });
    })
    .catch(error => console.error('Error fetching images:', error));
});
