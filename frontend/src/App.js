import React, { useState } from 'react';

function App() {
  const [selectedPoet, setSelectedPoet] = useState('');
  const [selectedTheme, setSelectedTheme] = useState('');
  const [generatedPoem, setGeneratedPoem] = useState('');
  const [emotions, setEmotions] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const poets = [
    { id: 'William Shakespeare', name: 'William Shakespeare' },
    { id: 'Robert Frost', name: 'Robert Frost' },
    { id: 'Emily Dickinson', name: 'Emily Dickinson' },
    { id: 'Edgar Allan Poe', name: 'Edgar Allan Poe' }
  ];

  const themes = [
    { id: 'nature', name: 'Nature' },
    { id: 'love', name: 'Love' },
    { id: 'death', name: 'Death' },
    { id: 'time', name: 'Time' },
    { id: 'seasons', name: 'Seasons' },
    { id: 'hope', name: 'Hope' },
    { id: 'sadness', name: 'Sadness' },
    { id: 'joy', name: 'Joy' }
  ];

  const generatePoem = async () => {
    setLoading(true);
    setError(null);
    setGeneratedPoem('');
    setEmotions(null);
    
    try {
      console.log('Sending request with poet:', selectedPoet, 'and theme:', selectedTheme);
      
      const response = await fetch('http://localhost:5000/generate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          poet: selectedPoet,
          theme: selectedTheme
        }),
      });

      const data = await response.json();
      
      if (!response.ok) {
        throw new Error(data.error || 'Failed to generate poem');
      }

      console.log('Response received:', data);

      if (data.poem) {
        setGeneratedPoem(data.poem);
        if (data.emotions) {
          setEmotions(data.emotions);
        }
      } else {
        throw new Error('No poem in response');
      }
    } catch (err) {
      console.error('Generation error:', err);
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto p-4">
      <div className="bg-white shadow rounded-lg p-6">
        <h1 className="text-2xl font-bold mb-4">Poetry Generation System</h1>
        
        {error && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
            Error: {error}
          </div>
        )}
        
        <div className="space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block mb-2">Select Poet Style</label>
              <select 
                value={selectedPoet} 
                onChange={(e) => setSelectedPoet(e.target.value)}
                className="w-full p-2 border rounded"
              >
                <option value="">Choose a poet...</option>
                {poets.map(poet => (
                  <option key={poet.id} value={poet.id}>
                    {poet.name}
                  </option>
                ))}
              </select>
            </div>

            <div>
              <label className="block mb-2">Select Theme</label>
              <select 
                value={selectedTheme} 
                onChange={(e) => setSelectedTheme(e.target.value)}
                className="w-full p-2 border rounded"
              >
                <option value="">Choose a theme...</option>
                {themes.map(theme => (
                  <option key={theme.id} value={theme.id}>
                    {theme.name}
                  </option>
                ))}
              </select>
            </div>
          </div>

          <button 
            onClick={generatePoem} 
            disabled={!selectedPoet || !selectedTheme || loading}
            className="w-full bg-blue-500 text-white p-2 rounded disabled:bg-gray-300"
          >
            {loading ? 'Generating...' : 'Generate Poem'}
          </button>

          {generatedPoem && (
            <div className="space-y-4">
              <div className="bg-gray-50 p-4 rounded whitespace-pre-line">
                {generatedPoem}
              </div>

              {emotions && (
                <div>
                  <h3 className="text-lg font-semibold mb-2">Emotional Analysis</h3>
                  <div className="grid grid-cols-2 gap-4 mt-4">
                    {Object.entries(emotions).map(([emotion, score]) => (
                      <div key={emotion} className="bg-gray-50 p-2 rounded">
                        <div className="font-semibold capitalize">{emotion}</div>
                        <div className="w-full bg-gray-200 rounded-full h-2.5">
                          <div
                            className="bg-blue-600 h-2.5 rounded-full"
                            style={{ width: `${score * 100}%` }}
                          />
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;