import { Request, Response, NextFunction } from 'express';

import { ApiResponse, ERROR_CODES, HTTP_STATUS } from '@teams-bot/shared';

/**
 * Simple authentication middleware
 * In production, this should validate JWT tokens from Azure AD or your auth provider
 */
export const authenticate = (req: Request, res: Response, next: NextFunction): void => {
  // For now, we'll use a simple header-based auth
  // TODO: Implement proper JWT validation with Azure AD B2C or Teams SSO
  const authHeader = req.headers.authorization;

  if (!authHeader) {
    const response: ApiResponse = {
      success: false,
      error: {
        code: ERROR_CODES.UNAUTHORIZED,
        message: 'Authentication required',
      },
    };

    res.status(HTTP_STATUS.UNAUTHORIZED).json(response);
    return;
  }

  // Extract user info from token (mock for now)
  // In production, decode and verify JWT
  const token = authHeader.replace('Bearer ', '');

  // Mock user extraction - replace with real JWT decode
  (req as any).user = {
    id: token || 'mock-user-id',
    teamsId: 'mock-teams-id',
    name: 'Mock User',
    email: 'user@example.com',
  };

  next();
};

/**
 * Optional authentication - doesn't fail if no auth provided
 */
export const optionalAuth = (req: Request, _res: Response, next: NextFunction): void => {
  const authHeader = req.headers.authorization;

  if (authHeader) {
    const token = authHeader.replace('Bearer ', '');
    (req as any).user = {
      id: token || 'mock-user-id',
      teamsId: 'mock-teams-id',
      name: 'Mock User',
      email: 'user@example.com',
    };
  }

  next();
};
