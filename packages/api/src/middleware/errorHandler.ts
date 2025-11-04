import { Request, Response, NextFunction } from 'express';

import { ApiResponse, ERROR_CODES, HTTP_STATUS } from '@teams-bot/shared';

import { logger } from '../utils/logger';

export class AppError extends Error {
  constructor(
    public statusCode: number,
    public code: string,
    message: string,
    public details?: any
  ) {
    super(message);
    this.name = 'AppError';
    Error.captureStackTrace(this, this.constructor);
  }
}

export const errorHandler = (
  err: Error,
  req: Request,
  res: Response,
  _next: NextFunction
): void => {
  logger.error('Error occurred:', {
    error: err.message,
    stack: err.stack,
    path: req.path,
    method: req.method,
  });

  if (err instanceof AppError) {
    const response: ApiResponse = {
      success: false,
      error: {
        code: err.code,
        message: err.message,
        details: err.details,
      },
      metadata: {
        timestamp: new Date().toISOString(),
        requestId: req.headers['x-request-id'] as string,
      },
    };

    res.status(err.statusCode).json(response);
    return;
  }

  // Mongoose validation errors
  if (err.name === 'ValidationError') {
    const response: ApiResponse = {
      success: false,
      error: {
        code: ERROR_CODES.VALIDATION_ERROR,
        message: 'Validation failed',
        details: err.message,
      },
    };

    res.status(HTTP_STATUS.BAD_REQUEST).json(response);
    return;
  }

  // Mongoose cast errors (invalid ObjectId)
  if (err.name === 'CastError') {
    const response: ApiResponse = {
      success: false,
      error: {
        code: ERROR_CODES.INVALID_INPUT,
        message: 'Invalid ID format',
      },
    };

    res.status(HTTP_STATUS.BAD_REQUEST).json(response);
    return;
  }

  // Default server error
  const response: ApiResponse = {
    success: false,
    error: {
      code: ERROR_CODES.INTERNAL_ERROR,
      message: 'An unexpected error occurred',
    },
    metadata: {
      timestamp: new Date().toISOString(),
      requestId: req.headers['x-request-id'] as string,
    },
  };

  res.status(HTTP_STATUS.INTERNAL_SERVER_ERROR).json(response);
};
