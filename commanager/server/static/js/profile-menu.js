document.addEventListener("DOMContentLoaded", function () {
    const avatar = document.querySelector(".avatar");
    const profileMenu = document.querySelector(".profile-menu");

    if (!avatar || !profileMenu) return; // safely exit if elements are missing

    avatar.addEventListener("click", (event) => {
        event.stopPropagation(); // prevent click from bubbling to document
        profileMenu.classList.toggle("active");

        // Positioning logic (optional, if floating menu)
        const { bottom, right } = avatar.getBoundingClientRect();
        profileMenu.style.position = "absolute";
        profileMenu.style.top = `${bottom + 10}px`;
        profileMenu.style.left = `${right - profileMenu.offsetWidth}px`;
    });

    // Close the menu if clicking outside
    document.addEventListener("click", (event) => {
        if (!avatar.contains(event.target) && !profileMenu.contains(event.target)) {
            profileMenu.classList.remove("active");
        }
    });
});
