"use client";

import React, { useState, useRef, useEffect, useImperativeHandle, forwardRef } from "react";
import Convert from "ansi-to-html";
import { DirectoryPicker } from "./DirectoryPicker";

const convert = new Convert({
    fg: '#f8fafc',
    bg: 'transparent',
    newline: true,
    escapeXML: true,
    stream: true
});

type Message = {
  role: "user" | "assistant";
  content: string;
};

type Session = {
    id: string;
    name: string;
    messages: Message[];
    cwd: string;
};

interface ChatPanelProps {
  agentName: string;
  width: number;
  onResize: (delta: number) => void;
  placeholder?: string;
  sessionId: string;
  autoPrompt?: string | null;
  mode?: "agent" | "direct"; // New mode prop
  projectRoot: string | null;
}

export interface ChatPanelHandle {
    injectMessage: (message: string) => void;
}

export const ChatPanel = forwardRef<ChatPanelHandle, ChatPanelProps>(({ agentName, width, placeholder = "Send instruction...", sessionId: viewId, autoPrompt, mode = "agent", projectRoot }, ref) => {
  const [sessions, setSessions] = useState<Session[]>([]);
  const [activeSessionId, setActiveSessionId] = useState<string>("");
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [apiKey, setApiKey] = useState("");
  const [model, setModel] = useState("claude-3-5-haiku-latest");
  const [cwd, setCwd] = useState("~");
  const [showSettings, setShowSettings] = useState(false);
  const [showDirPicker, setShowDirPicker] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const autoPromptSent = useRef<Record<string, boolean>>({});

  useImperativeHandle(ref, () => ({
    injectMessage: (msg: string) => {
        handleAutoSend(msg);
    }
  }));

  useEffect(() => {
    const savedKey = localStorage.getItem("anthropic_api_key");
    if (savedKey) setApiKey(savedKey);
    const savedModel = localStorage.getItem("anthropic_model");
    if (savedModel) setModel(savedModel);
  }, []);

  useEffect(() => {
    const savedSessions = localStorage.getItem(`sessions_${viewId}`);
    if (savedSessions) {
        let parsed = JSON.parse(savedSessions);
        // Migration: Ensure all IDs are strings and look unique (simple check)
        // If we see duplicate IDs or number-like strings that might collide, regen them.
        const seenIds = new Set();
        parsed = parsed.map((s: any) => {
            if (!s.id || seenIds.has(s.id) || !isNaN(Number(s.id))) {
                s.id = crypto.randomUUID();
            }
            seenIds.add(s.id);
            return s;
        });
        
        if (parsed.length > 0) {
            setSessions(parsed);
            setActiveSessionId(parsed[0].id);
            const parts = (parsed[0].cwd || "~").split("/");
            setCwd(parts[parts.length - 1] || "~");
            return;
        }
    }
    createNewSession();
  }, [viewId]);

  useEffect(() => {
    if (sessions.length > 0) {
        localStorage.setItem(`sessions_${viewId}`, JSON.stringify(sessions));
    }
  }, [sessions, viewId]);

  useEffect(() => {
    if (autoPrompt && apiKey && activeSessionId && !autoPromptSent.current[activeSessionId]) {
        const session = sessions.find(s => s.id === activeSessionId);
        if (session && session.messages.length === 1) {
            autoPromptSent.current[activeSessionId] = true;
            handleAutoSend(autoPrompt);
        }
    }
  }, [autoPrompt, apiKey, activeSessionId, sessions]);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [activeSessionId, sessions]);

  useEffect(() => {
    if (projectRoot && activeSession && activeSession.cwd !== projectRoot && apiKey) {
        handleDirSelect(projectRoot);
    }
  }, [projectRoot, activeSessionId, apiKey]);

  const createNewSession = () => {
    const newSession: Session = {
        id: crypto.randomUUID(),
        name: `Session ${new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}`,
        messages: [{ role: "assistant", content: mode === "agent" ? `System initialized. ${agentName} ready.` : "Direct connection established. Commands ready." }],
        cwd: "~"
    };
    setSessions(prev => [newSession, ...prev]);
    setActiveSessionId(newSession.id);
    setCwd("~");
  };

  const activeSession = sessions.find(s => s.id === activeSessionId) || sessions[0];

  const updateActiveSession = (messages: Message[], newCwd?: string) => {
    setSessions(prev => prev.map(s => 
        s.id === activeSessionId 
            ? { ...s, messages, cwd: newCwd || s.cwd } 
            : s
    ));
    if (newCwd) {
        const parts = newCwd.split("/");
        setCwd(parts[parts.length - 1] || "~");
    }
  };

  const saveSettings = () => {
    localStorage.setItem("anthropic_api_key", apiKey);
    localStorage.setItem("anthropic_model", model);
    setShowSettings(false);
  };

  const handleAutoSend = async (msgContent: string) => {
    if (!apiKey) return;
    
    setSessions(prev => {
        const currentActive = prev.find(s => s.id === activeSessionId);
        if (!currentActive) return prev;
        const newMsg: Message = { role: "user", content: msgContent };
        const updatedMessages = [...currentActive.messages, newMsg];
        triggerNetworkCall(updatedMessages);
        return prev.map(s => s.id === activeSessionId ? { ...s, messages: updatedMessages } : s);
    });
    setIsLoading(true);
  };

  const triggerNetworkCall = async (updatedMessages: Message[]) => {
    try {
      const response = await fetch("/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          messages: updatedMessages.map(m => ({ role: m.role, content: m.content })),
          apiKey,
          model,
          sessionId: activeSessionId
        })
      });
      const data = await response.json();
      if (data.error) {
        updateActiveSession([...updatedMessages, { role: "assistant", content: `Error: ${data.error}` }]);
      } else {
        let newCwdRaw = activeSession?.cwd || "~";
        if (data.session?.cwd) newCwdRaw = data.session.cwd;
        let text = Array.isArray(data.content) ? data.content.find((c: any) => c.type === "text")?.text || "No text" : data.content;
        updateActiveSession([...updatedMessages, { role: "assistant", content: text }], newCwdRaw);
      }
    } catch (error: any) {
      updateActiveSession([...updatedMessages, { role: "assistant", content: `Connection Error: ${error.message}` }]);
    } finally {
      setIsLoading(false);
    }
  };

  const sendMessage = async () => {
    if (!input.trim()) return;
    if (!apiKey) { setShowSettings(true); return; }
    await handleAutoSend(input);
    setInput("");
  };

  const handleDirSelect = async (path: string) => {
      setShowDirPicker(false);
      if (!apiKey || !activeSessionId) return;

      setIsLoading(true);
      try {
          const response = await fetch("/api/chat", {
              method: "POST",
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify({
                  apiKey,
                  sessionId: activeSessionId,
                  systemAction: { type: "set_cwd", path }
              })
          });
          const data = await response.json();
          if (data.session?.cwd) {
              const parts = data.session.cwd.split("/");
              setCwd(parts[parts.length - 1] || "/");
              
              // Add a system message to chat
              const systemMsg: Message = { role: "assistant", content: `System: Working directory changed to ${data.session.cwd}` };
              updateActiveSession([...activeSession.messages, systemMsg], data.session.cwd);
          }
      } catch (e) {
          console.error("Failed to update CWD", e);
      } finally {
          setIsLoading(false);
      }
  };

  return (
    <div className="chat-panel glass h-full w-full flex flex-row overflow-hidden min-h-0">
      <div className="session-sidebar flex flex-col h-full shrink-0 border-r border-white/10 bg-black/40 shadow-xl" style={{ width: '220px' }}>
        <div className="panel-label flex justify-between items-center p-4 border-b border-white/10 shrink-0 bg-black/20">
            <span className="text-[10px] tracking-[0.2em] font-black text-[var(--color-accent-orange)] uppercase">History</span>
            <button onClick={createNewSession} className="w-6 h-6 flex items-center justify-center rounded-md bg-white/5 border border-white/10 text-[var(--color-accent-orange)] font-black text-lg hover:bg-[var(--color-accent-orange)] hover:text-black transition-all">+</button>
        </div>
        <div className="flex-grow overflow-y-auto custom-scrollbar">
            {sessions.map(s => (
                <div key={s.id} className={`group relative p-4 border-b border-white/[0.05] cursor-pointer transition-all ${activeSessionId === s.id ? 'bg-[var(--color-accent-orange)]/10 border-r-2 border-r-[var(--color-accent-orange)]' : 'hover:bg-white/5'}`} onClick={() => { setActiveSessionId(s.id); const parts = (s.cwd || "~").split("/"); setCwd(parts[parts.length-1] || "~"); }}>
                    <div className="font-mono text-[8px] opacity-30 mb-1.5 tracking-[0.1em]">{s.id}</div>
                    <div className={`truncate text-[10px] font-bold tracking-wider uppercase ${activeSessionId === s.id ? 'text-[var(--color-accent-orange)]' : 'text-[var(--color-text-dim)]'}`}>{s.name}</div>
                </div>
            ))}
        </div>
      </div>

      <div className="flex-grow flex flex-col min-w-0 h-full relative bg-black/10">
        {showSettings && (
            <div className="fixed inset-0 z-[100] flex items-center justify-center bg-black/70 backdrop-blur-md">
                <div className="glass p-8 w-[500px] flex flex-col gap-6 shadow-2xl border-[var(--color-accent-orange)]/30">
                    <h2 className="text-xl font-bold text-[var(--color-accent-orange)] tracking-[0.3em] uppercase border-b border-white/10 pb-4">Auth_Settings</h2>
                    <div className="flex flex-col gap-3">
                        <label className="text-[10px] font-mono uppercase text-[var(--color-text-dim)] tracking-widest">Anthropic_API_Key</label>
                        <input type="password" value={apiKey} onChange={(e) => setApiKey(e.target.value)} className="bg-black/60 border border-white/10 p-4 rounded text-white font-mono text-sm focus:border-[var(--color-accent-orange)] outline-none transition-all" placeholder="sk-ant-..."/>
                    </div>
                    <div className="flex flex-col gap-3">
                        <label className="text-[10px] font-mono uppercase text-[var(--color-text-dim)] tracking-widest">Model_Identifier</label>
                        <input type="text" value={model} onChange={(e) => setModel(e.target.value)} className="bg-black/60 border border-white/10 p-4 rounded text-white font-mono text-sm focus:border-[var(--color-accent-orange)] outline-none transition-all" />
                    </div>
                    <div className="flex justify-end gap-4 mt-4">
                        <button onClick={() => setShowSettings(false)} className="px-6 py-2 hover:bg-white/10 rounded transition-colors text-xs uppercase font-bold tracking-widest">Cancel</button>
                        <button onClick={saveSettings} className="bg-[var(--color-accent-orange)] text-black px-8 py-2 rounded font-black hover:brightness-125 transition-all text-xs uppercase shadow-[0_0_20px_rgba(249,115,22,0.2)]">Save_Changes</button>
                    </div>
                </div>
            </div>
        )}

        {showDirPicker && <DirectoryPicker onSelect={handleDirSelect} onCancel={() => setShowDirPicker(false)} />}

        <div className="p-4 border-b border-white/10 flex justify-between items-center shrink-0 bg-black/40 backdrop-blur-sm">
            <div className="flex flex-col gap-0.5">
                <span className="text-[9px] font-black tracking-[0.3em] text-[var(--color-accent-orange)] uppercase opacity-80">
                    {mode === "agent" ? "Agent_Persona" : "Direct_Link"}
                </span>
                <span className="font-bold tracking-[0.1em] text-xs truncate uppercase text-[var(--color-text-main)]">
                    {agentName} <span className="opacity-30 mx-2">//</span> <span className="text-[var(--color-text-dim)] text-[10px] lowercase italic font-normal">{activeSession?.name}</span>
                </span>
            </div>
            <button onClick={() => setShowSettings(true)} className="text-[9px] font-mono text-[var(--color-accent-orange)] hover:brightness-125 uppercase shrink-0 tracking-widest bg-[var(--color-accent-orange)]/10 px-3 py-1.5 rounded border border-[var(--color-accent-orange)]/20 shadow-sm">
                {apiKey ? "Link_Active" : "Configure_Auth"}
            </button>
        </div>

        <div className="flex-grow overflow-y-auto font-mono text-sm min-h-0 custom-scrollbar">
            {activeSession?.messages.map((msg, idx) => (
            <div key={idx} className={`p-6 border-b border-white/[0.03] ${msg.role === "assistant" ? "bg-white/[0.015]" : ""}`}>
                <div className="flex items-center gap-3 mb-3 opacity-40 text-[9px] uppercase tracking-[0.2em] font-black">
                    <span className={msg.role === "assistant" ? "text-[var(--color-accent-orange)]" : "text-white"}>{msg.role === "assistant" ? "CLAUDE" : "USER"}</span>
                    <span className="w-1 h-1 bg-white/20 rounded-full"></span>
                    <span>{new Date().toLocaleTimeString()}</span>
                </div>
                <div className="whitespace-pre-wrap leading-[1.7] text-[14px] text-[#e2e8f0] font-mono" dangerouslySetInnerHTML={{ __html: msg.role === "assistant" ? convert.toHtml(msg.content) : msg.content }} />
            </div>
            ))}
            {isLoading && <div className="p-6 opacity-40 animate-pulse font-mono text-[10px] uppercase tracking-[0.3em] flex items-center gap-4"><span className="w-2 h-2 bg-[var(--color-accent-orange)] rounded-full"></span>Processing_Request...</div>}
            <div ref={messagesEndRef} />
        </div>

        <div className="chat-input shrink-0 bg-black/80 border-t border-white/10 p-5 shadow-[0_-10px_30px_rgba(0,0,0,0.5)]">
            <div className="flex items-center gap-4">
                <button onClick={() => setShowDirPicker(true)} className="font-mono text-[var(--color-accent-orange)] font-black text-xs whitespace-nowrap bg-[var(--color-accent-orange)]/10 border border-[var(--color-accent-orange)]/20 px-3 py-1.5 rounded flex items-center gap-2 shadow-[0_0_10px_rgba(249,115,22,0.1)] hover:bg-[var(--color-accent-orange)]/20 transition-colors cursor-pointer">
                    <span className="opacity-50 text-[10px]">DIR:</span>{cwd} <span className="text-white/30 ml-1">❯</span>
                </button>
                <input type="text" placeholder={placeholder} className="outline-none w-grow bg-transparent font-mono text-[var(--color-text-main)] placeholder:text-white/10 text-sm tracking-wide flex-grow" value={input} onChange={(e) => setInput(e.target.value)} onKeyDown={(e) => e.key === "Enter" && sendMessage()} autoFocus />
            </div>
        </div>
      </div>
    </div>
  );
});

ChatPanel.displayName = "ChatPanel";
