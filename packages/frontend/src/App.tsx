import { FluentProvider, webLightTheme, tokens } from '@fluentui/react-components';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { Layout } from './components/Layout';
import { BotGallery } from './pages/BotGallery';
import { BotCreator } from './pages/BotCreator';
import { BotChat } from './pages/BotChat';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: 1,
    },
  },
});

function App() {
  return (
    <FluentProvider theme={webLightTheme}>
      <QueryClientProvider client={queryClient}>
        <BrowserRouter>
          <Routes>
            <Route path="/" element={<Layout />}>
              <Route index element={<Navigate to="/bots" replace />} />
              <Route path="bots" element={<BotGallery />} />
              <Route path="bots/new" element={<BotCreator />} />
              <Route path="bots/:botId/chat" element={<BotChat />} />
            </Route>
          </Routes>
        </BrowserRouter>
      </QueryClientProvider>
    </FluentProvider>
  );
}

export default App;
