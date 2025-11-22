import type { User } from '../utils/auth';

export interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
}

export interface LoginCredentials {
  email: string;
  password: string;
}

export interface ActivityData {
  date: string;
  visits: number;
  actions: number;
}

export interface ActionCategory {
  category: string;
  count: number;
}

export interface UserListItem {
  id: string;
  name: string;
  email: string;
  role: 'admin' | 'user';
  status: 'active' | 'inactive';
  lastLogin: string;
}
