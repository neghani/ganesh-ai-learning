import { http, HttpResponse } from 'msw';
import type { LoginCredentials, ActivityData, ActionCategory, UserListItem } from '../types/index';
import type { User } from '../utils/auth';
import { createMockToken } from '../utils/auth';

// Mock users
const mockUsers: User[] = [
  {
    id: '1',
    email: 'user@demo.com',
    name: 'John Doe',
    role: 'user',
  },
  {
    id: '2',
    email: 'admin@demo.com',
    name: 'Admin User',
    role: 'admin',
  },
  {
    id: '6',
    email: 'admin2@demo.com',
    name: 'Super Admin',
    role: 'admin',
  },
];

// Mock activity data
const mockActivityData: ActivityData[] = [
  { date: '2024-01-15', visits: 120, actions: 45 },
  { date: '2024-01-16', visits: 135, actions: 52 },
  { date: '2024-01-17', visits: 98, actions: 38 },
  { date: '2024-01-18', visits: 156, actions: 67 },
  { date: '2024-01-19', visits: 142, actions: 58 },
  { date: '2024-01-20', visits: 178, actions: 73 },
  { date: '2024-01-21', visits: 165, actions: 69 },
];

const mockActionCategories: ActionCategory[] = [
  { category: 'Profile View', count: 45 },
  { category: 'Settings Update', count: 23 },
  { category: 'Data Export', count: 12 },
  { category: 'Report Generation', count: 8 },
  { category: 'Other', count: 15 },
];

// Mock users list for admin
const mockUsersList: UserListItem[] = [
  {
    id: '1',
    name: 'John Doe',
    email: 'user@demo.com',
    role: 'user',
    status: 'active',
    lastLogin: '2024-01-21T10:30:00Z',
  },
  {
    id: '2',
    name: 'Admin User',
    email: 'admin@demo.com',
    role: 'admin',
    status: 'active',
    lastLogin: '2024-01-21T09:15:00Z',
  },
  {
    id: '3',
    name: 'Jane Smith',
    email: 'jane@demo.com',
    role: 'user',
    status: 'active',
    lastLogin: '2024-01-20T16:45:00Z',
  },
  {
    id: '4',
    name: 'Bob Johnson',
    email: 'bob@demo.com',
    role: 'user',
    status: 'inactive',
    lastLogin: '2024-01-18T14:20:00Z',
  },
  {
    id: '5',
    name: 'Alice Brown',
    email: 'alice@demo.com',
    role: 'user',
    status: 'active',
    lastLogin: '2024-01-21T08:30:00Z',
  },
];

export const handlers = [
  // Auth endpoints
  http.post('/api/auth/login', async ({ request }) => {
    const credentials = await request.json() as LoginCredentials;
    
    const user = mockUsers.find(u => u.email === credentials.email);
    
    if (!user || credentials.password !== 'password123') {
      return HttpResponse.json(
        { message: 'Invalid credentials' },
        { status: 401 }
      );
    }
    
    const token = createMockToken(user);
    
    return HttpResponse.json({
      user,
      token,
    });
  }),

  http.get('/api/auth/me', ({ request }) => {
    const authHeader = request.headers.get('Authorization');
    if (!authHeader || !authHeader.startsWith('Bearer ')) {
      return HttpResponse.json(
        { message: 'No token provided' },
        { status: 401 }
      );
    }
    
    // In a real app, you'd validate the token here
    // For demo purposes, we'll just return a mock user
    
    return HttpResponse.json({
      user: mockUsers[0], // Return first user for demo
    });
  }),

  // User dashboard endpoints
  http.get('/api/user/activity', () => {
    return HttpResponse.json({
      activityData: mockActivityData,
      actionCategories: mockActionCategories,
    });
  }),

  // Admin dashboard endpoints
  http.get('/api/admin/users', () => {
    return HttpResponse.json({
      users: mockUsersList,
    });
  }),
];
