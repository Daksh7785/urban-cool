import React, { useState } from 'react';
import axios from 'axios';
import { Send, Bot, User, ShieldAlert } from 'lucide-react';

export default function Copilot() {
  const [messages, setMessages] = useState([{ sender: 'bot', text: 'I am the UrbanOS AI Copilot. How can I assist you with climate resilience planning today?' }]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const sendMessage = async () => {
    if (!input.trim()) return;

    const newMessages = [...messages, { sender: 'user', text: input }];
    setMessages(newMessages);
    setInput('');
    setIsLoading(true);

    try {
      // Phase 9: AI Copilot RAG Integration Call
      const res = await axios.post('http://localhost:5000/api/copilot/chat', { message: input });
      setMessages([...newMessages, { sender: 'bot', text: res.data.reply }]);
    } catch (e) {
      setMessages([...newMessages, { sender: 'bot', text: "Error: Copilot is currently offline. Please ensure the UrbanOS Backend is running." }]);
    }
    
    setIsLoading(false);
  };

  return (
    <div className="flex flex-col h-[calc(100vh-5rem)] bg-slate-50">
      <div className="p-4 border-b bg-white flex items-center space-x-3">
        <Bot className="text-blue-600" size={24} />
        <div>
          <h2 className="text-lg font-bold text-slate-800">Climate Copilot</h2>
          <p className="text-xs text-slate-500">RAG Architecture powered by IPCC & NASA Datasets</p>
        </div>
      </div>

      <div className="flex-1 overflow-y-auto p-6 space-y-6">
        {messages.map((msg, idx) => (
          <div key={idx} className={`flex ${msg.sender === 'user' ? 'justify-end' : 'justify-start'}`}>
            <div className={`flex items-start max-w-2xl space-x-3 ${msg.sender === 'user' ? 'flex-row-reverse space-x-reverse' : ''}`}>
              <div className={`p-2 rounded-full ${msg.sender === 'user' ? 'bg-blue-100' : 'bg-slate-200'}`}>
                {msg.sender === 'user' ? <User size={20} className="text-blue-700"/> : <Bot size={20} className="text-slate-700"/>}
              </div>
              <div className={`p-4 rounded-lg shadow-sm ${msg.sender === 'user' ? 'bg-blue-600 text-white' : 'bg-white text-slate-800 border border-slate-200'}`}>
                {msg.text}
              </div>
            </div>
          </div>
        ))}
        {isLoading && (
          <div className="flex justify-start">
            <div className="bg-white border border-slate-200 p-4 rounded-lg text-slate-500 animate-pulse">
              Analyzing climate data...
            </div>
          </div>
        )}
      </div>

      <div className="p-4 bg-white border-t">
        <div className="flex space-x-4 max-w-4xl mx-auto">
          <input 
            type="text" 
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
            placeholder="Ask about hotspots, request policy generation, or summarize the latest data..."
            className="flex-1 border border-slate-300 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <button 
            onClick={sendMessage}
            className="bg-blue-600 text-white p-3 rounded-lg hover:bg-blue-700 transition flex items-center justify-center">
            <Send size={24} />
          </button>
        </div>
      </div>
    </div>
  );
}
