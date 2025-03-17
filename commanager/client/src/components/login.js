import React from 'react';
import './styles/login_signup.css'; // Import your CSS

function Login() {
  return (
    <div className="container">
      <div className="Login_SignUp">
        <h2>Login</h2>
        <form action="/login" method="POST">
          <div className="select-wrapper">
            <select name="user_type">
              <option value="" disabled selected>
                Select Artist or Client
              </option>
              <option value="artist">Artist</option>
              <option value="client">Client</option>
            </select>
          </div>
          <div className="name-container">
            <input type="text" name="first_name" placeholder="First name" />
            <input type="text" name="last_name" placeholder="Last name" />
          </div>
          <input type="email" name="email" placeholder="Email address" />
          <input type="password" name="password" placeholder="Password" />
          <button type="submit" className="Button">
            Login
          </button>
        </form>

        <p className="switch">
          New user? <a href="signup.html">Click here to sign up now!</a>
        </p>
      </div>
    </div>
  );
}

export default Login;