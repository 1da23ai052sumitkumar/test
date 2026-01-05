import { Routes, Route } from "react-router-dom";
import Signup from "./pages/signup";
import Signin from "./pages/signin";
import Dashboard from "./pages/dashboard";
function App() {
  return (
    <Routes>
      <Route path="/" element={<Dashboard />} />
      <Route path="/signup" element={<Signup />} />
      <Route path="/signin" element={<Signin />} />
    </Routes>
  );
}

export default App;
