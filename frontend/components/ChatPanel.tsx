"use client";

import React, { useState, useRef, useEffect } from "react";

type Message = {
  role: "user" | "assistant";
  content: string;
};

interface ChatPanelProps {
  agentName: string;
  width: number;
  onResize: (delta: number) => void;
  placeholder?: string;
}

export function ChatPanel({ agentName, width, placeholder = "Send instruction..." }: ChatPanelProps) {
  const [messages, setMessages] = useState<Message[]>([
    { role: "assistant", content: `System initialized. ${agentName} ready. Please configure your API Key to begin.` }
  ]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [apiKey, setApiKey] = useState("");
  const [model, setModel] = useState("claude-3-5-haiku-latest");
  const [showSettings, setShowSettings] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const savedKey = localStorage.getItem("anthropic_api_key");
    if (savedKey) setApiKey(savedKey);
    const savedModel = localStorage.getItem("anthropic_model");
    if (savedModel) setModel(savedModel);
  }, []);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const saveSettings = () => {
    localStorage.setItem("anthropic_api_key", apiKey);
    localStorage.setItem("anthropic_model", model);
    setShowSettings(false);
  };

  const sendMessage = async () => {
    if (!input.trim()) return;
    if (!apiKey) {
      setShowSettings(true);
      return;
    }

    const newMsg: Message = { role: "user", content: input };
    setMessages(prev => [...prev, newMsg]);
    setInput("");
    setIsLoading(true);

    try {
      const response = await fetch("/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          messages: [...messages, newMsg].map(m => ({ role: m.role, content: m.content })),
          apiKey,
          model
        })
      });

      const data = await response.json();
      
      if (data.error) {
        setMessages(prev => [...prev, { role: "assistant", content: `Error: ${data.error}` }]);
      } else {
        let text = "";
        if (Array.isArray(data.content)) {
            text = data.content.find((c: any) => c.type === "text")?.text || "No text response";
        } else {
            text = data.content;
        }
        setMessages(prev => [...prev, { role: "assistant", content: text }]);
      }
    } catch (error: any) {
      setMessages(prev => [...prev, { role: "assistant", content: `Connection Error: ${error.message}` }]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="chat-panel glass h-full relative" style={{ width: `${width}px`, minWidth: '200px' }}>
      {/* Settings Modal */}
      {showSettings && (
        <div className="fixed inset-0 z-[100] flex items-center justify-center bg-black/60 backdrop-blur-sm">
          <div className="glass p-8 w-[500px] flex flex-col gap-4">
            <h2 className="text-xl font-bold text-[var(--color-accent-orange)]">AUTHENTICATION</h2>
            <p className="text-[var(--color-text-dim)] text-sm">
              Please provide your Anthropic API Key to enable the Claude agent.
            </p>
            
            <div className="flex flex-col gap-2">
                <label className="text-xs font-mono uppercase text-[var(--color-text-dim)]">API Key</label>
                <input 
                    type="password" 
                    value={apiKey} 
                    onChange={(e) => setApiKey(e.target.value)}
                    className="bg-black/40 border border-[var(--color-border)] p-3 rounded text-white font-mono"
                    placeholder="sk-ant-..."
                />
            </div>

            <div className="flex flex-col gap-2">
                <label className="text-xs font-mono uppercase text-[var(--color-text-dim)]">Model ID</label>
                <input 
                    type="text" 
                    value={model} 
                    onChange={(e) => setModel(e.target.value)}
                    className="bg-black/40 border border-[var(--color-border)] p-3 rounded text-white font-mono"
                    placeholder="claude-3-5-haiku-latest"
                />
            </div>

            <div className="flex flex-col gap-2 opacity-50 cursor-not-allowed">
                <label className="text-xs font-mono uppercase text-[var(--color-text-dim)]">Subscription OAuth (Claude Code)</label>
                <div className="bg-black/40 border border-[var(--color-border)] p-3 rounded text-[var(--color-text-dim)] font-mono text-left flex justify-between items-center text-sm">
                    <span>Connect with Claude...</span>
                    <span className="text-[10px] bg-[var(--color-border)] px-2 py-1 rounded">COMING SOON</span>
                </div>
            </div>

            <div className="flex justify-end gap-3 mt-4">
                <button 
                    onClick={() => setShowSettings(false)}
                    className="px-4 py-2 hover:bg-white/10 rounded transition-colors text-sm"
                >
                    Cancel
                </button>
                <button 
                    onClick={saveSettings}
                    className="bg-[var(--color-accent-orange)] text-white px-6 py-2 rounded font-bold hover:brightness-110 transition-all text-sm"
                >
                    Save Settings
                </button>
            </div>
          </div>
        </div>
      )}

      <div className="p-4 border-b border-[var(--color-border)] flex justify-between items-center shrink-0">
          <span className="font-bold tracking-wider text-sm">AGENT_LINK</span>
          <button 
              onClick={() => setShowSettings(true)}
              className="text-[10px] font-mono text-[var(--color-accent-orange)] hover:underline"
          >
              {apiKey ? "CONNECTED" : "CONFIGURE_AUTH"}
          </button>
      </div>

      <div className="chat-messages flex-grow overflow-y-auto">
        {messages.map((msg, idx) => (
          <div key={idx} className={msg.role === "assistant" ? "msg-agent" : "mb-6 text-right px-4"}>
            {msg.role === "assistant" && <strong className="block mb-2 text-[var(--color-accent-orange)] text-xs uppercase tracking-widest">CLAUDE::{agentName}</strong>}
            <div className={msg.role === "user" ? "inline-block bg-white/10 p-4 rounded-xl rounded-tr-none text-left text-base" : "text-base"}>
              {msg.content}
            </div>
          </div>
        ))}
        {isLoading && (
          <div className="msg-agent opacity-50 animate-pulse">
              <strong className="block mb-2 text-[var(--color-accent-orange)] text-xs uppercase tracking-widest">CLAUDE::{agentName}</strong>
              <div className="text-base italic">Processing...</div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <div className="chat-input shrink-0">
        <input 
          type="text" 
          placeholder={placeholder} 
          className="outline-none w-full bg-transparent" 
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && sendMessage()}
        />
      </div>
    </div>
  );
}
