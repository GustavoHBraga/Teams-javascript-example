import { useQuery } from '@tanstack/react-query';
import { useNavigate } from 'react-router-dom';
import {
  makeStyles,
  tokens,
  Card,
  CardHeader,
  Text,
  Button,
  Spinner,
  Badge,
  Title2,
} from '@fluentui/react-components';
import { ChatRegular, EditRegular } from '@fluentui/react-icons';
import { botApi } from '../services/botService';
import type { Bot } from '@teams-bot/shared';

const useStyles = makeStyles({
  container: {
    padding: '24px',
    maxWidth: '1400px',
    margin: '0 auto',
  },
  header: {
    marginBottom: '24px',
  },
  grid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fill, minmax(350px, 1fr))',
    gap: '20px',
  },
  card: {
    height: '100%',
    cursor: 'pointer',
    transition: 'transform 0.2s',
    ':hover': {
      transform: 'translateY(-4px)',
      boxShadow: tokens.shadow16,
    },
  },
  cardContent: {
    padding: '16px',
    display: 'flex',
    flexDirection: 'column',
    gap: '12px',
  },
  description: {
    color: tokens.colorNeutralForeground2,
    minHeight: '40px',
  },
  tags: {
    display: 'flex',
    gap: '8px',
    flexWrap: 'wrap',
  },
  actions: {
    display: 'flex',
    gap: '8px',
    marginTop: '8px',
  },
  loading: {
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
    height: '400px',
  },
  empty: {
    textAlign: 'center',
    padding: '60px 20px',
  },
});

export function BotGallery() {
  const styles = useStyles();
  const navigate = useNavigate();

  const { data, isLoading, error } = useQuery({
    queryKey: ['bots'],
    queryFn: () => botApi.list(),
  });

  if (isLoading) {
    return (
      <div className={styles.loading}>
        <Spinner label="Carregando bots..." size="large" />
      </div>
    );
  }

  if (error) {
    return (
      <div className={styles.container}>
        <Text>Erro ao carregar bots. Verifique se a API está rodando.</Text>
      </div>
    );
  }

  const bots = data?.items || [];

  return (
    <div className={styles.container}>
      <div className={styles.header}>
        <Title2>Meus Bots ({bots.length})</Title2>
      </div>

      {bots.length === 0 ? (
        <div className={styles.empty}>
          <Title2>Nenhum bot criado ainda</Title2>
          <Text>Clique em "Criar Bot" para começar!</Text>
        </div>
      ) : (
        <div className={styles.grid}>
          {bots.map((bot: Bot) => (
            <Card key={bot.id} className={styles.card}>
              <CardHeader
                header={<Text weight="semibold">{bot.name}</Text>}
                description={
                  <Badge
                    appearance="tint"
                    color={bot.status === 'active' ? 'success' : 'warning'}
                  >
                    {bot.status}
                  </Badge>
                }
              />
              
              <div className={styles.cardContent}>
                <Text className={styles.description}>{bot.description}</Text>

                {bot.tags && bot.tags.length > 0 && (
                  <div className={styles.tags}>
                    {bot.tags.map((tag) => (
                      <Badge key={tag} size="small">
                        {tag}
                      </Badge>
                    ))}
                  </div>
                )}

                <Text size={200} style={{ color: tokens.colorNeutralForeground3 }}>
                  {bot.conversationCount} conversas • {bot.scope}
                </Text>

                <div className={styles.actions}>
                  <Button
                    appearance="primary"
                    icon={<ChatRegular />}
                    onClick={(e) => {
                      e.stopPropagation();
                      navigate(`/bots/${bot.id}/chat`);
                    }}
                  >
                    Conversar
                  </Button>
                  <Button
                    icon={<EditRegular />}
                    onClick={(e) => {
                      e.stopPropagation();
                      alert('Edição em desenvolvimento');
                    }}
                  >
                    Editar
                  </Button>
                </div>
              </div>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
}
