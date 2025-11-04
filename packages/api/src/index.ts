import express, { Express } from 'express';
import cors from 'cors';
import helmet from 'helmet';
import 'express-async-errors';

import { config, validateConfig } from './config';
import { connectDatabase } from './database/connection';
import { logger } from './utils/logger';
import { errorHandler } from './middleware';
import { requestId } from './middleware/helpers';
import routes from './routes';

// Validate configuration
validateConfig();

// Create Express app
const app: Express = express();

// Security middleware
app.use(helmet());
app.use(
  cors({
    origin: config.corsOrigins,
    credentials: true,
  })
);

// Body parsing middleware
app.use(express.json({ limit: '10mb' }));
app.use(express.urlencoded({ extended: true }));

// Request ID middleware
app.use(requestId);

// API routes
app.use('/api/v1', routes);

// Error handling middleware (must be last)
app.use(errorHandler);

// Start server
async function startServer() {
  try {
    // Connect to database
    await connectDatabase();

    // Start listening
    app.listen(config.port, config.host, () => {
      logger.info(`🚀 API server running on http://${config.host}:${config.port}`);
      logger.info(`📝 Environment: ${config.env}`);
      logger.info(`🔗 Health check: http://${config.host}:${config.port}/api/v1/health`);
    });
  } catch (error) {
    logger.error('Failed to start server:', error);
    process.exit(1);
  }
}

// Handle graceful shutdown
process.on('SIGTERM', () => {
  logger.info('SIGTERM signal received: closing HTTP server');
  process.exit(0);
});

process.on('SIGINT', () => {
  logger.info('SIGINT signal received: closing HTTP server');
  process.exit(0);
});

// Start the server
startServer();

export default app;
