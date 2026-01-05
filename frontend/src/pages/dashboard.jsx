import { useState } from "react";
import { useNavigate } from "react-router-dom";
import "../styles/dashboard.css";

function Dashboard() {
  const navigate = useNavigate();

  // simulate login state (later replace with JWT)
  const [isLoggedIn, setIsLoggedIn] = useState(true);

  const handleAuthClick = () => {
    if (isLoggedIn) {
      // logout
      setIsLoggedIn(false);
      navigate("/signin");
    } else {
      navigate("/signin");
    }
  };

  return (
    <div>
      <nav className="navbar">
        <h2 className="logo">MyApp</h2>

        <ul className="nav-links">
          <li onClick={() => navigate("/")}>Home</li>
          <li onClick={() => navigate("/signup")}>signup</li>
          <li onClick={handleAuthClick}>
            {isLoggedIn ? "Logout" : "Login"}
          </li>
        </ul>
      </nav>

      <div className="content">
        <h1>Welcome to Dashboard</h1>
        <p>This is the home page of your dashboard.</p>
      </div>
    </div>
  );
}

export default Dashboard;
