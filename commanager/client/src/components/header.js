document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("header").innerHTML = `
        <header>
            <div class="header">
                <a href="home.html" class="logo">
                    <div class="logo-header">
                        <img src="./image/pinterest.png" alt="logo-image" class="logo-image">
                    </div>
                    <p class="logo-text">commanager</p>
                </a>
                <div class="search-bar">
                    <input type="text" class="search-box" placeholder="Search">
                </div>
                <div class="user">
                    <a href="{{ url_for('user_profile', username=username) }}">
                        <div class="username-text">{{ username }}</div>
                    </a>
                </div>
                <div class="avatar"></div>
            </div>    
        </header>
    `;

    const avatar = document.querySelector(".avatar");
    const profileMenu = document.createElement("div");

    profileMenu.classList.add("profile-menu");
    profileMenu.innerHTML = `
        <ul>
            <li><a href="user.html">View Profile</a></li>
            <li><a href="orders.html">Orders</a></li>
            <li><a href="messages.html">Messages</a></li>
            <li><a href="settings.html">Settings</a></li>
            <li><a href="login.html">Login</a></li>
        </ul>
    `;
    document.body.appendChild(profileMenu);
    
    avatar.addEventListener("click", (event) => {
        profileMenu.classList.toggle("active");
        const { bottom, right } = avatar.getBoundingClientRect();
        profileMenu.style.top = `${bottom + 10}px`;
        profileMenu.style.left = `${right - profileMenu.offsetWidth}px`;
    });

    // Close the menu if clicked outside
    document.addEventListener("click", (event) => {
        if (!avatar.contains(event.target) && !profileMenu.contains(event.target)) {
            profileMenu.classList.remove("active");
        }
    });
});