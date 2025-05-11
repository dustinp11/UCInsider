// utils/Ask.js
const LOCAL_URL = 'http://localhost:5000';
const API_URL = process.env.REACT_APP_API_URL || LOCAL_URL;

export async function fetchAnswer(question) {
  try {
    const res = await fetch(`${API_URL}/ask`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ question }),
    });
    const { response, summary } = await res.json();

    // Combine into one block
    return `${response}\n\n${summary}`;
  } catch (err) {
    console.error('Error fetching answer:', err);
    return 'Something went wrong.';
  }
}
