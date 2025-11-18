import { useEffect, useRef } from 'react';

interface ChainlitEmbedProps {
  userId?: string;
  metadata?: Record<string, string | number | boolean | object>;
  height?: string;
}

export const ChainlitEmbed: React.FC<ChainlitEmbedProps> = ({
  userId,
  metadata = {},
  height = '600px'
}) => {
  const iframeRef = useRef<HTMLIFrameElement>(null);

  useEffect(() => {
    if (!iframeRef.current) return;

    const handleIframeLoad = () => {
      const iframeWindow = iframeRef.current?.contentWindow;
      if (!iframeWindow) return;

      const contextData = {
        userId: "342erw9843jwrp9ruw93",
        userEmail: "user@example.com",
        sessionId: sessionStorage.getItem('sessionId'),
        timestamp: Date.now(),
        ...metadata
      };

      iframeWindow.postMessage(
        JSON.stringify(contextData),
        import.meta.env.VITE_CHAINLIT_URL
      );
    };

    const iframe = iframeRef.current;
    iframe.addEventListener('load', handleIframeLoad);

    const handleMessage = (event: MessageEvent) => {
      if (event.origin !== import.meta.env.VITE_CHAINLIT_URL) return;

      console.log('Message from Chainlit:', event.data);
      try {
        const data = JSON.parse(event.data);
        if (data.status === 'received') {
          console.log('Chainlit received context:', data.context);
        }
      } catch {
        console.log('Non-JSON message from Chainlit:', event.data);
      }
    };

    window.addEventListener('message', handleMessage);

    return () => {
      iframe.removeEventListener('load', handleIframeLoad);
      window.removeEventListener('message', handleMessage);
    };
  }, [userId, metadata]);

  return (
    <div className="chainlit-container">
      <iframe
        ref={iframeRef}
        src={import.meta.env.VITE_CHAINLIT_URL}
        title="Chainlit Chat"
        width="100%"
        height={height}
        frameBorder="0"
        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
        allowFullScreen
        style={{
          borderRadius: '8px',
          boxShadow: '0 2px 8px rgba(0,0,0,0.1)'
        }}
      />
    </div>
  );
};
