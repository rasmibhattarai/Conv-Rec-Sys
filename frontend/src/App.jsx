import { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import { Send, Bot, User, Cpu } from 'lucide-react';
import Markdown from 'markdown-to-jsx';
import './index.css';

function App() {
  const [messages, setMessages] = useState([
    { role: 'assistant', content: 'Welcome to the Appliance Recommender! How can I help you today?' }
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [sessionId, setSessionId] = useState(null);
  const [preferences, setPreferences] = useState({
    categories: [],
    budget: null,
    mandatory_filters: [],
    soft_preferences: []
  });

  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    const userMessage = input.trim();
    setInput('');
    setMessages(prev => [...prev, { role: 'user', content: userMessage }]);
    setIsLoading(true);

    try {
      const response = await axios.post('http://localhost:8000/chat', {
        session_id: sessionId,
        message: userMessage
      });

      setSessionId(response.data.session_id);
      setMessages(prev => [...prev, { role: 'assistant', content: response.data.response }]);
      setPreferences(response.data.state);
    } catch (error) {
      console.error('Error fetching response:', error);
      setMessages(prev => [...prev, { role: 'assistant', content: 'Sorry, I encountered an error. Please try again.' }]);
    } finally {
      setIsLoading(false);
    }
  };

  const PreferenceBadge = ({ label, items }) => {
    if (!items || (Array.isArray(items) && items.length === 0)) return null;
    
    return (
      <div className="mb-4 text-left">
        <h3 className="text-sm font-semibold text-gray-500 uppercase tracking-wider mb-2">{label}</h3>
        <div className="flex flex-wrap gap-2">
          {Array.isArray(items) ? (
            items.map((item, idx) => (
              <span key={idx} className="bg-blue-100 text-blue-800 text-xs font-medium px-2.5 py-1 rounded-full">
                {item}
              </span>
            ))
          ) : (
            <span className="bg-green-100 text-green-800 text-xs font-medium px-2.5 py-1 rounded-full">
              {items}
            </span>
          )}
        </div>
      </div>
    );
  };

  return (
    <div className="flex h-screen bg-gray-50 text-left !w-full !max-w-none !border-none !flex-row">
      {/* Sidebar for Tracked Preferences */}
      <div className="w-64 bg-white border-r border-gray-200 p-6 flex flex-col h-full overflow-y-auto shrink-0">
        <div className="flex items-center gap-2 mb-8 text-left">
          <Cpu className="text-blue-600" size={24} />
          <h1 className="text-xl font-bold text-gray-800 !m-0 !tracking-normal !text-left">Appliance AI</h1>
        </div>

        <div className="flex-1 text-left">
          <h2 className="text-lg font-semibold text-gray-700 mb-4 pb-2 border-b border-gray-100 !m-0 !tracking-normal">
            Tracked Preferences
          </h2>
          
          <div className="space-y-6 mt-4">
            <PreferenceBadge label="Categories" items={preferences.categories} />
            <PreferenceBadge label="Budget" items={preferences.budget} />
            <PreferenceBadge label="Must-Have Features" items={preferences.mandatory_filters} />
            <PreferenceBadge label="Nice-to-Have Features" items={preferences.soft_preferences} />

            {(!preferences.categories?.length && !preferences.budget && !preferences.mandatory_filters?.length && !preferences.soft_preferences?.length) && (
              <p className="text-sm text-gray-400 italic text-left">
                No preferences tracked yet. Chat to set them!
              </p>
            )}
          </div>
        </div>
      </div>

      {/* Main Chat Area */}
      <div className="flex-1 flex flex-col h-full overflow-hidden w-full bg-gray-50">
        {/* Messages */}
        <div className="flex-1 overflow-y-auto p-4 md:p-8 space-y-6">
          {messages.map((msg, index) => (
            <div
              key={index}
              className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'} w-full max-w-4xl mx-auto`}
            >
              <div className={`flex gap-4 max-w-[80%] ${msg.role === 'user' ? 'flex-row-reverse' : 'flex-row'}`}>
                <div className={`w-8 h-8 rounded-full flex items-center justify-center shrink-0 ${
                  msg.role === 'user' ? 'bg-blue-600 text-white' : 'bg-green-600 text-white'
                }`}>
                  {msg.role === 'user' ? <User size={16} /> : <Bot size={16} />}
                </div>
                
                <div className={`rounded-2xl px-5 py-4 ${
                  msg.role === 'user' 
                    ? 'bg-blue-600 text-white rounded-tr-none text-left' 
                    : 'bg-white border border-gray-200 text-gray-800 shadow-sm rounded-tl-none prose prose-sm max-w-none text-left'
                }`}>
                  {msg.role === 'user' ? (
                    msg.content
                  ) : (
                    <Markdown>{msg.content}</Markdown>
                  )}
                </div>
              </div>
            </div>
          ))}
          
          {isLoading && (
            <div className="flex justify-start w-full max-w-4xl mx-auto">
              <div className="flex gap-4 max-w-[80%]">
                <div className="w-8 h-8 rounded-full bg-green-600 text-white flex items-center justify-center shrink-0">
                  <Bot size={16} />
                </div>
                <div className="bg-white border border-gray-200 rounded-2xl rounded-tl-none px-5 py-4 shadow-sm flex items-center">
                  <div className="flex gap-1">
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0ms' }} />
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '150ms' }} />
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '300ms' }} />
                  </div>
                </div>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        {/* Input Area */}
        <div className="bg-white border-t border-gray-200 p-4">
          <div className="max-w-4xl mx-auto">
            <form onSubmit={handleSubmit} className="relative flex items-center w-full">
              <input
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                placeholder="Ask about appliances..."
                className="w-full pl-4 pr-12 py-3 rounded-xl border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-white text-gray-900 shadow-sm"
                disabled={isLoading}
              />
              <button
                type="submit"
                disabled={!input.trim() || isLoading}
                className="absolute right-2 p-2 text-blue-600 hover:bg-blue-50 rounded-lg disabled:opacity-50 disabled:hover:bg-transparent transition-colors cursor-pointer"
              >
                <Send size={20} />
              </button>
            </form>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
