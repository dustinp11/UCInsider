// Utility function to send question to the backend and get a response
export async function fetchAnswer(question) {

    const isProduction = process.env.NODE_ENV === 'production';

  if (isProduction) {
    // Temporarily return a dummy response instead of calling backend
    return `This is a placeholder answer for: "${question}" — backend not deployed.`;
  }

  try {
    const res = await fetch('http://localhost:5000/ask', {
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
