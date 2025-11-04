import dotenv from 'dotenv';

dotenv.config();

export const config = {
  // Server
  env: process.env.NODE_ENV || 'development',
  port: parseInt(process.env.PORT || '3001', 10),
  host: process.env.HOST || '0.0.0.0',

  // Database
  mongodbUri: process.env.MONGODB_URI || 'mongodb://localhost:27017/teams-bot-automation',

  // Azure OpenAI / OpenAI
  openai: {
    azureApiKey: process.env.AZURE_OPENAI_API_KEY,
    azureEndpoint: process.env.AZURE_OPENAI_ENDPOINT,
    azureDeploymentName: process.env.AZURE_OPENAI_DEPLOYMENT_NAME || 'gpt-4',
    azureApiVersion: process.env.AZURE_OPENAI_API_VERSION || '2024-02-01',
    apiKey: process.env.OPENAI_API_KEY,
  },

  // Azure Storage
  storage: {
    connectionString: process.env.AZURE_STORAGE_CONNECTION_STRING || '',
    containerName: process.env.AZURE_STORAGE_CONTAINER_NAME || 'bot-documents',
  },

  // Azure AI Search
  search: {
    endpoint: process.env.AZURE_SEARCH_ENDPOINT || '',
    apiKey: process.env.AZURE_SEARCH_API_KEY || '',
    indexName: process.env.AZURE_SEARCH_INDEX_NAME || 'bot-documents-index',
  },

  // Security
  jwtSecret: process.env.JWT_SECRET || 'change-this-secret-in-production',
  corsOrigins: (process.env.CORS_ORIGINS || 'http://localhost:3000').split(','),

  // Rate Limiting
  rateLimit: {
    windowMs: parseInt(process.env.RATE_LIMIT_WINDOW_MS || '60000', 10),
    maxRequests: parseInt(process.env.RATE_LIMIT_MAX_REQUESTS || '100', 10),
  },

  // Logging
  logLevel: process.env.LOG_LEVEL || 'info',

  // File Upload
  maxFileSize: parseInt(process.env.MAX_FILE_SIZE || '10485760', 10), // 10MB
} as const;

// Validate required configuration
export function validateConfig() {
  const required = ['mongodbUri'];

  const missing = required.filter((key) => {
    const value = config[key as keyof typeof config];
    return !value || (typeof value === 'string' && value.trim() === '');
  });

  if (missing.length > 0) {
    throw new Error(`Missing required configuration: ${missing.join(', ')}`);
  }

  // Warn if using default secrets
  if (config.jwtSecret === 'change-this-secret-in-production' && config.env === 'production') {
    console.warn('⚠️  WARNING: Using default JWT secret in production!');
  }
}
