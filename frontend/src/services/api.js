export const searchProjectInfo = async (query) => {
  const response = await fetch('http://localhost:8000/api/search', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ query }),
  });
  
  if (!response.ok) {
    throw new Error('Search request failed');
  }
  
  return response.json();
};

export const fetchSearchHistory = async () => {
  const response = await fetch('http://localhost:8000/api/history');
  if (!response.ok) {
    throw new Error('Failed to fetch history');
  }
  return response.json();
};
