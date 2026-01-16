'use client';

import { useState, useRef, useEffect } from 'react';
import styles from './page.module.css';

interface Message {
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
}

export default function Home() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    const userMessage: Message = {
      role: 'user',
      content: input.trim(),
      timestamp: new Date(),
    };

    // Prepare conversation history before adding new message (to avoid including it twice)
    // Convert messages to the format expected by the backend (role and content only)
    const conversationHistory = messages.map((msg) => ({
      role: msg.role,
      content: msg.content,
    }));

    setMessages((prev) => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      // Determine the API URL
      // In development, use localhost. In production (Vercel), use relative URLs
      const isDevelopment = typeof window !== 'undefined' && 
        (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1');
      
      // Use relative URL in production (same domain), or localhost in development
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || 
        (isDevelopment ? 'http://localhost:8000' : '');
      
      // Build the API endpoint
      // If apiUrl is empty (production without NEXT_PUBLIC_API_URL), use relative URL
      const apiEndpoint = apiUrl ? `${apiUrl}/api/chat` : '/api/chat';
      
      const response = await fetch(apiEndpoint, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 
          message: userMessage.content,
          conversation_history: conversationHistory
        }),
      });

      if (!response.ok) {
        // Try to get error details from the response
        let errorDetail = `HTTP error! status: ${response.status}`;
        try {
          const errorData = await response.json();
          if (errorData.detail) {
            errorDetail = errorData.detail;
          }
        } catch (e) {
          // If response is not JSON, use the default error message
        }
        throw new Error(errorDetail);
      }

      const data = await response.json();
      const assistantMessage: Message = {
        role: 'assistant',
        content: data.reply,
        timestamp: new Date(),
      };

      setMessages((prev) => [...prev, assistantMessage]);
    } catch (error) {
      console.error('Error sending message:', error);
      // Extract error message from the error object
      const errorMessageText = error instanceof Error 
        ? error.message 
        : 'Sorry, I encountered an error. Please try again later.';
      
      const errorMessage: Message = {
        role: 'assistant',
        content: `⚠️ ${errorMessageText}`,
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <main className={styles.container}>
      <div className={styles.chatContainer}>
        <header className={styles.header}>
          <h1 className={styles.title}>🧠 Mental Coach</h1>
          <p className={styles.subtitle}>Your supportive AI companion</p>
        </header>

        <div className={styles.messagesContainer}>
          {messages.length === 0 ? (
            <div className={styles.welcomeMessage}>
              <p>Welcome! I'm here to support you.</p>
              <p>Feel free to share what's on your mind, and I'll do my best to help.</p>
            </div>
          ) : (
            messages.map((message, index) => (
              <div
                key={index}
                className={`${styles.message} ${
                  message.role === 'user' ? styles.userMessage : styles.assistantMessage
                }`}
              >
                <div className={styles.messageContent}>
                  <div className={styles.messageRole}>
                    {message.role === 'user' ? 'You' : 'Coach'}
                  </div>
                  <div className={styles.messageText}>{message.content}</div>
                </div>
              </div>
            ))
          )}
          {isLoading && (
            <div className={`${styles.message} ${styles.assistantMessage}`}>
              <div className={styles.messageContent}>
                <div className={styles.messageRole}>Coach</div>
                <div className={styles.loadingDots}>
                  <span></span>
                  <span></span>
                  <span></span>
                </div>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        <form onSubmit={handleSend} className={styles.inputForm}>
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Type your message here..."
            className={styles.input}
            disabled={isLoading}
          />
          <button
            type="submit"
            className={styles.sendButton}
            disabled={isLoading || !input.trim()}
          >
            Send
          </button>
        </form>
      </div>
    </main>
  );
}
