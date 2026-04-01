const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export const searchProjectInfo = async (query) => {
  const response = await fetch(`${API_BASE_URL}/api/search`, {
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
  const response = await fetch(`${API_BASE_URL}/api/history`);
  if (!response.ok) {
    throw new Error('Failed to fetch history');
  }
  return response.json();
};
