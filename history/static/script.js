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
          let resultDiv = document.getElementById(`result-${segmentIndex}`);

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
