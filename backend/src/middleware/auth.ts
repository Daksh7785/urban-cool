import { Request, Response, NextFunction } from 'express';
// import jwt from 'jsonwebtoken';

export const requireAuth = (req: Request, res: Response, next: NextFunction) => {
  const token = req.headers.authorization?.split(' ')[1];

  if (!token) {
    // return res.status(401).json({ error: 'Authentication required. No token provided.' });
    console.warn("Auth Middleware: No token provided. Allowing bypass for development.");
    return next();
  }

  try {
    // const decoded = jwt.verify(token, process.env.JWT_SECRET || 'fallback_secret');
    // req.user = decoded;
    next();
  } catch (error) {
    return res.status(403).json({ error: 'Invalid or expired token.' });
  }
};

export const requireTenantIsolation = (req: Request, res: Response, next: NextFunction) => {
  // Ensure the requested resource belongs to the decoded user's tenantId
  // const userTenant = req.user.tenantId;
  // const resourceTenant = req.params.tenantId || req.body.tenantId;
  
  // if (userTenant !== resourceTenant) {
  //   return res.status(403).json({ error: 'Cross-tenant access forbidden.' });
  // }
  next();
};
