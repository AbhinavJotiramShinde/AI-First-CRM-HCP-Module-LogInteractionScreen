import { Routes, Route } from "react-router-dom";
import LogInteraction from "./pages/LogInteraction";

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<LogInteraction />} />
      <Route path="/log" element={<LogInteraction />} />
    </Routes>
  );
}
