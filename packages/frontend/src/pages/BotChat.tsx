import { useState, useRef, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useQuery, useMutation } from '@tanstack/react-query';
import {
  makeStyles,
  tokens,
  Card,
  Input,
  Button,
  Text,
  Spinner,
  Avatar,
  Title3,
} from '@fluentui/react-components';
import { SendRegular, ArrowLeftRegular, BotRegular, PersonRegular } from '@fluentui/react-icons';
import { botApi, chatApi } from '../services/botService';

const useStyles = makeStyles({
  container: {
    display: 'flex',
    flexDirection: 'column',
    height: 'calc(100vh - 73px)',
    maxWidth: '1200px',
    margin: '0 auto',
  },
  header: {
    padding: '16px 24px',
    borderBottom: `1px solid ${tokens.colorNeutralStroke1}`,
    backgroundColor: tokens.colorNeutralBackground1,
    display: 'flex',
    alignItems: 'center',
    gap: '16px',
  },
  messages: {
    flex: 1,
    overflow: 'auto',
    padding: '24px',
    display: 'flex',
    flexDirection: 'column',
    gap: '16px',
  },
  messageCard: {
    maxWidth: '70%',
    padding: '12px 16px',
  },
  userMessage: {
    alignSelf: 'flex-end',
    backgroundColor: tokens.colorBrandBackground,
    color: tokens.colorNeutralForegroundOnBrand,
  },
  botMessage: {
    alignSelf: 'flex-start',
    backgroundColor: tokens.colorNeutralBackground1,
  },
  messageHeader: {
    display: 'flex',
    alignItems: 'center',
    gap: '8px',
    marginBottom: '8px',
  },
  inputArea: {
    padding: '16px 24px',
    borderTop: `1px solid ${tokens.colorNeutralStroke1}`,
    backgroundColor: tokens.colorNeutralBackground1,
    display: 'flex',
    gap: '12px',
  },
  loading: {
    display: 'flex',
    justifyContent: 'center',
    padding: '40px',
  },
});

export function BotChat() {
  const styles = useStyles();
  const { botId } = useParams<{ botId: string }>();
  const navigate = useNavigate();
  const [message, setMessage] = useState('');
  const [messages, setMessages] = useState<any[]>([]);
  const [conversationId, setConversationId] = useState<string>();
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const { data: bot, isLoading: loadingBot } = useQuery({
    queryKey: ['bot', botId],
    queryFn: () => botApi.getById(botId!),
    enabled: !!botId,
  });

  const sendMutation = useMutation({
    mutationFn: (content: string) => chatApi.sendMessage(botId!, content, conversationId),
    onSuccess: (data) => {
      setMessages((prev) => [
        ...prev,
        {
          role: 'user',
          content: data.userMessage.content,
          createdAt: data.userMessage.createdAt,
        },
        {
          role: 'assistant',
          content: data.assistantMessage.content,
          createdAt: data.assistantMessage.createdAt,
        },
      ]);
      setConversationId(data.conversation.id);
      setMessage('');
    },
  });

  const handleSend = () => {
    if (message.trim()) {
      sendMutation.mutate(message);
    }
  };

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  if (loadingBot) {
    return (
      <div className={styles.loading}>
        <Spinner label="Carregando bot..." size="large" />
      </div>
    );
  }

  return (
    <div className={styles.container}>
      <div className={styles.header}>
        <Button
          appearance="subtle"
          icon={<ArrowLeftRegular />}
          onClick={() => navigate('/bots')}
        />
        <Avatar icon={<BotRegular />} color="brand" />
        <div>
          <Title3>{bot?.name}</Title3>
          <Text size={200} style={{ color: tokens.colorNeutralForeground3 }}>
            {bot?.description}
          </Text>
        </div>
      </div>

      <div className={styles.messages}>
        {messages.length === 0 && (
          <div style={{ textAlign: 'center', padding: '60px 20px' }}>
            <Text size={400}>Inicie uma conversa com {bot?.name}!</Text>
          </div>
        )}

        {messages.map((msg, index) => (
          <Card
            key={index}
            className={`${styles.messageCard} ${
              msg.role === 'user' ? styles.userMessage : styles.botMessage
            }`}
          >
            <div className={styles.messageHeader}>
              <Avatar
                icon={msg.role === 'user' ? <PersonRegular /> : <BotRegular />}
                size={24}
                color={msg.role === 'user' ? 'colorful' : 'brand'}
              />
              <Text weight="semibold" size={200}>
                {msg.role === 'user' ? 'Você' : bot?.name}
              </Text>
            </div>
            <Text>{msg.content}</Text>
          </Card>
        ))}

        {sendMutation.isPending && (
          <Card className={`${styles.messageCard} ${styles.botMessage}`}>
            <Spinner size="tiny" label={`${bot?.name} está pensando...`} />
          </Card>
        )}

        <div ref={messagesEndRef} />
      </div>

      <div className={styles.inputArea}>
        <Input
          style={{ flex: 1 }}
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          placeholder="Digite sua mensagem..."
          onKeyPress={(e) => e.key === 'Enter' && handleSend()}
          disabled={sendMutation.isPending}
        />
        <Button
          appearance="primary"
          icon={<SendRegular />}
          onClick={handleSend}
          disabled={!message.trim() || sendMutation.isPending}
        >
          Enviar
        </Button>
      </div>
    </div>
  );
}
