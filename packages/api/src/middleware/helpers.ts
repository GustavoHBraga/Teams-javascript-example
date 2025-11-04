import { Request, Response, NextFunction } from 'express';
import { v4 as uuidv4 } from 'uuid';

import { ApiResponse } from '@teams-bot/shared';

/**
 * Add request ID to each request
 */
export const requestId = (req: Request, _res: Response, next: NextFunction) => {
  req.headers['x-request-id'] = req.headers['x-request-id'] || uuidv4();
  next();
};

/**
 * Wrapper for async route handlers
 */
export const asyncHandler = (fn: Function) => {
  return (req: Request, res: Response, next: NextFunction) => {
    Promise.resolve(fn(req, res, next)).catch(next);
  };
};

/**
 * Standard success response
 */
export const sendSuccess = <T = any>(
  res: Response,
  data: T,
  statusCode: number = 200
): Response => {
  const response: ApiResponse<T> = {
    success: true,
    data,
    metadata: {
      timestamp: new Date().toISOString(),
      requestId: res.req.headers['x-request-id'] as string,
    },
  };

  return res.status(statusCode).json(response);
};
