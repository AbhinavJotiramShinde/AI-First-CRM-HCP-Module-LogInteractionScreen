import axios from "axios";
import { useDispatch } from "react-redux";
import { setAIExtracted } from "../features/interactionSlice";

export default function AIChatPanel() {
  const dispatch = useDispatch();

  const sendToAI = async (text) => {
    const res = await axios.post("http://localhost:8000/ai/parse", { text });
    dispatch(setAIExtracted(res.data.output));
  };

  return (
    <div>
      <textarea placeholder="Describe interaction..." />
      <button onClick={() => sendToAI("Met Dr Sharma today...")}>Ask AI</button>
    </div>
  );
}
