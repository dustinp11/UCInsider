// React component to ask a question and display RAG response
import React, { useState } from 'react';
import { fetchAnswer } from '../utils/Ask';

const Home = () => {
  const [question, setQuestion] = useState('');
  const [response, setResponse] = useState('');
  const [loading, setLoading] = useState(false);
  const [history, setHistory] = useState([]);


  const handleAsk = async () => {
    if (!question.trim()) return;
    setLoading(true);
    setResponse('');
  
    const answer = await fetchAnswer(question);
    setResponse(answer);

    setHistory((prev) => [...prev, { question, answer }]);
    setQuestion('');

    setLoading(false);
  };
  
  return (
    <div style={{ padding: '2rem', fontFamily: 'Arial' }}>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '1rem' }}>
        <h1 style={{ margin: 0 }}>Ask About a Class</h1>
        <img
          src="/images/zot.png"
          alt="Peter the Anteater"
          style={{ width: '100px', height: 'auto', marginLeft: '1rem' }}
        />
      </div>

      <input
        type="text"
        placeholder="e.g. Is ICS 31 a heavy workload?"
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
        onKeyDown={(e) => {
        if (e.key === 'Enter') {
          handleAsk();
        }
        }}
        style={{ width: '60%', padding: '0.5rem', fontSize: '1rem' }}
      />
      <button
        onClick={handleAsk}
        style={{ marginLeft: '1rem', padding: '0.5rem 1rem', fontSize: '1rem' }}
        disabled={loading}
      >
        {loading ? 'Asking...' : 'Ask'}
      </button>

      {response && (
        <div style={{ marginTop: '2rem', background: '#f4f4f4', padding: '1rem', whiteSpace: 'pre-wrap', fontFamily: 'Arial' }}>
          <h3>Answer:</h3>
          {response}
        </div>
      )}

      {history.length > 0 && (
  <div style={{ marginTop: '2rem', fontFamily: 'Arial' }}>
    <h3>Past Questions:</h3>
    <ul>
      {[...history].reverse().map((item, index) => (
        <li
          key={index}
          style={{
            marginBottom: '1rem',
            whiteSpace: 'pre-wrap', // 👈 keeps line breaks
          }}
        >
          <strong>Q:</strong> {item.question}
          <br />
          <strong>A:</strong> {item.answer}
        </li>
      ))}
    </ul>
  </div>
)}
    </div>
  );
};

export default Home;
