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
   const json = await res.json();

    if (json.response) {
      return json;          // return the full object
    }
    return { response: json.answer || '', summary: '' };
  } catch (err) {
    console.error('Error fetching answer:', err);
    return { response: '', summary: '' };
  }
}
