// React component to ask a question and display RAG response
import React, { useState } from 'react';
import { fetchAnswer } from '../utils/Ask';

const Home = () => {
  const [question, setQuestion] = useState('');
  const [response, setResponse] = useState('');
  const [loading, setLoading] = useState(false);

  const handleAsk = async () => {
    if (!question.trim()) return;
    setLoading(true);
    setResponse('');

    const answer = await fetchAnswer(question);
    setResponse(answer);
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
        <div style={{ marginTop: '2rem', background: '#f4f4f4', padding: '1rem' }}>
          <h3>Answer:</h3>
          <p>{response}</p>
        </div>
      )}
    </div>
  );
};

export default Home;
