import { Request, Response, NextFunction } from 'express';
import { ZodSchema, ZodError } from 'zod';

import { ApiResponse, ERROR_CODES, HTTP_STATUS } from '@teams-bot/shared';

/**
 * Validate request body against a Zod schema
 */
export const validateBody = (schema: ZodSchema) => {
  return (req: Request, res: Response, next: NextFunction): void => {
    try {
      req.body = schema.parse(req.body);
      next();
    } catch (error) {
      if (error instanceof ZodError) {
        const response: ApiResponse = {
          success: false,
          error: {
            code: ERROR_CODES.VALIDATION_ERROR,
            message: 'Validation failed',
            details: error.errors,
          },
        };

        res.status(HTTP_STATUS.BAD_REQUEST).json(response);
        return;
      }
      next(error);
    }
  };
};

/**
 * Validate query parameters against a Zod schema
 */
export const validateQuery = (schema: ZodSchema) => {
  return (req: Request, res: Response, next: NextFunction): void => {
    try {
      req.query = schema.parse(req.query);
      next();
    } catch (error) {
      if (error instanceof ZodError) {
        const response: ApiResponse = {
          success: false,
          error: {
            code: ERROR_CODES.VALIDATION_ERROR,
            message: 'Query validation failed',
            details: error.errors,
          },
        };

        res.status(HTTP_STATUS.BAD_REQUEST).json(response);
        return;
      }
      next(error);
    }
  };
};
