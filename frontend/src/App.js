import { useState } from "react";

const API_URL = process.env.REACT_APP_API_URL;

function App() {
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();

    await fetch(`${API_URL}/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        title,
        description,
        completed: false,
      }),
    });

    setTitle("");
    setDescription("");
  };

  return (
    <div style={{ padding: "20px" }}>
      <h1>Task Manager</h1>

      <form onSubmit={handleSubmit}>
        <div>
          <label>Task Name:</label>
          <input
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            required
          />
        </div>

        <div>
          <label>Task Description:</label>
          <input
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            required
          />
        </div>

        <button type="submit">Submit</button>
      </form>
    </div>
  );
}

export default App;
