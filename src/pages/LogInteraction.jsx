import { useState } from "react";
import axios from "axios";
import "../styles/log.css";

export default function LogInteraction() {
  const [aiInput, setAiInput] = useState("");
  const [form, setForm] = useState({
    hcp_name: "",
    topics: "",
    sentiment: "",
    samples_distributed: "",
    follow_ups: ""
  });

  const handleAI = async () => {
    try {
      const res = await axios.post("http://127.0.0.1:8000/chat/and-save", {
        message: aiInput
      });

      const i = res.data.interaction;

      setForm({
        hcp_name: i?.hcp_name || "",
        topics: Array.isArray(i?.topics) ? i.topics.join(", ") : (i?.topics || ""),
        sentiment: i?.sentiment || "",
        samples_distributed: i?.samples_distributed || "",
        follow_ups: Array.isArray(i?.follow_ups) ? i.follow_ups.join(", ") : (i?.follow_ups || "")
      });

      alert("✅ AI extracted & saved!");
    } catch (err) {
      console.error("AI error:", err);
      alert("❌ AI failed");
    }
  };

  return (
    <div className="log-container">
      {/* LEFT — AI Output (Read Only) */}
      <div className="left">
        <h2>Log HCP Interaction</h2>
        <input value={form.hcp_name} readOnly placeholder="HCP Name" />
        <input value={form.topics} readOnly placeholder="Topics" />
        <input value={form.sentiment} readOnly placeholder="Sentiment" />
        <input value={form.samples_distributed} readOnly placeholder="Samples Distributed" />
        <textarea value={form.follow_ups} readOnly placeholder="Follow Ups" />
      </div>

      {/* RIGHT — AI Input */}
      <div className="right">
        <h3>🤖 AI Assistant</h3>
        <textarea
          placeholder="Describe interaction..."
          value={aiInput}
          onChange={(e) => setAiInput(e.target.value)}
        />
        <button onClick={handleAI}>Log Interaction</button>
      </div>
    </div>
  );
}
