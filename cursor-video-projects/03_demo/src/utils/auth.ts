import { jwtDecode } from 'jwt-decode';

export interface User {
  id: string;
  email: string;
  name: string;
  role: 'admin' | 'user';
}

export interface JWTPayload {
  sub: string;
  email: string;
  name: string;
  role: 'admin' | 'user';
  iat: number;
  exp: number;
}

export const decodeToken = (token: string): JWTPayload | null => {
  try {
    return jwtDecode<JWTPayload>(token);
  } catch (error) {
    console.error('Failed to decode token:', error);
    return null;
  }
};

export const isTokenExpired = (token: string): boolean => {
  const decoded = decodeToken(token);
  if (!decoded) return true;
  
  const currentTime = Date.now() / 1000;
  return decoded.exp < currentTime;
};

export const getUserFromToken = (token: string): User | null => {
  const decoded = decodeToken(token);
  if (!decoded) return null;
  
  return {
    id: decoded.sub,
    email: decoded.email,
    name: decoded.name,
    role: decoded.role,
  };
};

export const createMockToken = (user: User): string => {
  const header = btoa(JSON.stringify({ alg: 'HS256', typ: 'JWT' }));
  const payload = btoa(JSON.stringify({
    sub: user.id,
    email: user.email,
    name: user.name,
    role: user.role,
    iat: Math.floor(Date.now() / 1000),
    exp: Math.floor(Date.now() / 1000) + (24 * 60 * 60), // 24 hours
  }));
  const signature = btoa('mock-signature');
  
  return `${header}.${payload}.${signature}`;
};
