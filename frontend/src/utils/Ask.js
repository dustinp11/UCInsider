// Utility function to send question to the backend and get a response
export async function fetchAnswer(question) {
  try {
    const res = await fetch('/ask', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ question }),
    });

    const data = await res.json();
    return data.answer || 'No answer returned.';
  } catch (err) {
    console.error('Error fetching answer:', err);
    return 'Something went wrong.';
  }
}
