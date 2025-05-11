// React component to ask a question and display RAG response
import React, { useState } from 'react';
import { fetchAnswer } from '../utils/Ask';

const Home = () => {
  const [question, setQuestion] = useState('');
  const [answerObj, setAnswerObj] = useState({ response: '', summary: '' });
  const [loading, setLoading] = useState(false);
  const [history, setHistory] = useState([]);

  const handleAsk = async () => {
    if (!question.trim()) return;
    setLoading(true);
    setAnswerObj({ response: '', summary: '' });

    const data = await fetchAnswer(question);
    setAnswerObj(data);

    setHistory(prev => [...prev, { question, ...data }]);
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
        onChange={e => setQuestion(e.target.value)}
        onKeyDown={e => e.key === 'Enter' && handleAsk()}
        style={{ width: '60%', padding: '0.5rem', fontSize: '1rem' }}
      />
      <button
        onClick={handleAsk}
        style={{ marginLeft: '1rem', padding: '0.5rem 1rem', fontSize: '1rem' }}
        disabled={loading}
      >
        {loading ? 'Asking...' : 'Ask'}
      </button>

      {(answerObj.response || answerObj.summary) && (
        <div style={{ marginTop: '2rem', background: '#f4f4f4', padding: '1rem', whiteSpace: 'pre-wrap' }}>
          {answerObj.response && (
            <>
              <h3>Full RAG Response:</h3>
              <p>{answerObj.response}</p>
            </>
          )}
          {answerObj.summary && (
            <>
              <h3>Refined Summary:</h3>
              <p>{answerObj.summary}</p>
            </>
          )}
        </div>
      )}

      {history.length > 0 && (
        <div style={{ marginTop: '2rem' }}>
          <h3>Past Questions:</h3>
          <ul>
            {[...history].reverse().map((item, i) => (
              <li key={i} style={{ marginBottom: '1rem', whiteSpace: 'pre-wrap' }}>
                <strong>Q:</strong> {item.question}
                <br />
                <strong>RAG:</strong> {item.response}
                <br />
                <strong>Summary:</strong> {item.summary}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

export default Home;
