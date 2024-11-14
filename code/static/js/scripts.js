/*!
* Start Bootstrap - Personal v1.0.1 (https://startbootstrap.com/template-overviews/personal)
* Copyright 2013-2023 Start Bootstrap
* Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-personal/blob/master/LICENSE)
*/
// This file is intentionally blank
// Use this file to add JavaScript to your project

function getRecommendations() {
    const bookTitle = document.getElementById("book_title").value;
    fetch('/recommend', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: `book_title=${encodeURIComponent(bookTitle)}`
    })
    .then(response => response.json())
    .then(data => {
        const recommendationsList = document.getElementById("recommendations");
        recommendationsList.innerHTML = "";
        data.forEach(rec => {
            const listItem = document.createElement("li");
            listItem.textContent = `${rec.Title} - Distance: ${rec.Distance.toFixed(4)}`;
            recommendationsList.appendChild(listItem);
        });
    });
}
