function ClientDashboard() {
    const [msg, setMsg] = useState("");
    const [reply, setReply] = useState("");
  
    const send = async () => {
      const res = await fetch("/api/v1/chat", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ message: msg, client_id: "demo" })
      });
      const data = await res.json();
      setReply(data.reply);
    };
  
    return (
      <>
        <textarea onChange={e => setMsg(e.target.value)} />
        <button onClick={send}>Send</button>
        <pre>{reply}</pre>
      </>
    );
  }
