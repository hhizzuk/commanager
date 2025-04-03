document.addEventListener("DOMContentLoaded", function () {
    // Popup Modal Functionality
    const commissionCards = document.querySelectorAll(".commission-card");
    const popup = document.getElementById("popup");
    const closePopup = document.getElementById("closePopup");

    commissionCards.forEach(card => {
        card.addEventListener("click", () => {
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