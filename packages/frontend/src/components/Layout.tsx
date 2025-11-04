import { Outlet, useNavigate, useLocation } from 'react-router-dom';
import {
  makeStyles,
  tokens,
  Button,
  Title3,
} from '@fluentui/react-components';
import { BotRegular, AddRegular, ChatRegular } from '@fluentui/react-icons';

const useStyles = makeStyles({
  root: {
    display: 'flex',
    flexDirection: 'column',
    height: '100vh',
  },
  header: {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'space-between',
    padding: '16px 24px',
    backgroundColor: tokens.colorNeutralBackground1,
    borderBottom: `1px solid ${tokens.colorNeutralStroke1}`,
  },
  headerLeft: {
    display: 'flex',
    alignItems: 'center',
    gap: '12px',
  },
  nav: {
    display: 'flex',
    gap: '8px',
  },
  main: {
    flex: 1,
    overflow: 'auto',
    backgroundColor: tokens.colorNeutralBackground2,
  },
});

export function Layout() {
  const styles = useStyles();
  const navigate = useNavigate();
  const location = useLocation();

  return (
    <div className={styles.root}>
      <header className={styles.header}>
        <div className={styles.headerLeft}>
          <BotRegular fontSize={28} />
          <Title3>Teams Bot Automation</Title3>
        </div>
        
        <nav className={styles.nav}>
          <Button
            appearance={location.pathname === '/bots' ? 'primary' : 'secondary'}
            icon={<ChatRegular />}
            onClick={() => navigate('/bots')}
          >
            Meus Bots
          </Button>
          <Button
            appearance={location.pathname === '/bots/new' ? 'primary' : 'secondary'}
            icon={<AddRegular />}
            onClick={() => navigate('/bots/new')}
          >
            Criar Bot
          </Button>
        </nav>
      </header>

      <main className={styles.main}>
        <Outlet />
      </main>
    </div>
  );
}
