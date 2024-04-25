function predict() {
        let temperature = document.getElementById('temperature').value;
        let time = document.getElementById('time').value;
        let Ux = document.getElementById('Ux').value;
        let Uy = document.getElementById('Uy').value;
        let Uz = document.getElementById('Uz').value;

        let data = {
            temperature: temperature == null || temperature === "" ? null : temperature,
            time: time == null || time === "" ? null : time,
            Ux: Ux.length === 0 ? null : Ux,
            Uy: Uy.length === 0 ? null : Uy,
            Uz: Uz.length === 0 ? null : Uz,
        };
        function send_data() {
          fetch('/predict', {method: 'POST', body: JSON.stringify(data)})
            .then(response => response.json())
            .then(respJson => {
              // Создаем URL для blob-объекта
              const imageObjectURL = URL.createObjectURL(imageBlob);
              // Вставляем изображение в div
              document.getElementById('imageContainer').innerHTML = `<img src="${imageObjectURL}" alt="Image" />`;
            });
        }

        send_data()

}


function clear_data() {
    document.getElementById('temperature').value = '';
    document.getElementById('time').value = '';
    document.getElementById('Ux').value = '';
    document.getElementById('Uy').value = '';
    document.getElementById('Uz').value = '';

}

document.addEventListener("DOMContentLoaded", () => {
    document.getElementById("applyButton").onclick = predict;
    document.getElementById("clearButton").onclick = clear_data;
})