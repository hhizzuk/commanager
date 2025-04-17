document.addEventListener("DOMContentLoaded", function () {
    const commissionCards = document.querySelectorAll(".commission-card");
    const popup = document.getElementById("popup");
    const closePopup = document.getElementById("closePopup");

    const popupTitle = document.querySelector(".popup-header");
    const popupDescription = document.getElementById("popupDescription");
    const popupImages = document.getElementById("popupImages");

    commissionCards.forEach(card => {
        card.addEventListener("click", () => {
            const title = card.getAttribute("data-title");
            const description = card.getAttribute("data-description");
            const price = card.getAttribute("data-price");
            const imageList = JSON.parse(card.getAttribute("data-images") || "[]");

            // Set title and description
            popupTitle.textContent = title;
            popupDescription.innerHTML = `
                ${description}<br><br><strong>Price:</strong> ${price}
            `;

            // Clear existing images
            popupImages.innerHTML = "";

            // Add each image dynamically
            imageList.forEach(url => {
                const img = document.createElement("img");
                img.src = url;
                img.className = "commission-image";
                img.alt = "Service image";
                popupImages.appendChild(img);
            });

            popup.style.display = "flex";
        });
    });

    closePopup.addEventListener("click", () => {
        popup.style.display = "none";
    });

    popup.addEventListener("click", event => {
        if (event.target === popup) {
            popup.style.display = "none";
        }
    });
});
