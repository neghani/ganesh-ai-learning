# Dashboard Application with Authentication

A modern React dashboard application with JWT-based authentication, separate user and admin views, built with TypeScript, Tailwind CSS, and Recharts.

## Features

- **Authentication**: JWT-based mock authentication system
- **User Dashboard**: Activity charts showing visits and actions over time
- **Admin Dashboard**: User management with detailed user list
- **Responsive Design**: Mobile-friendly interface with Tailwind CSS
- **Mock API**: MSW (Mock Service Worker) for API simulation

## Tech Stack

- **React 18** with TypeScript
- **Vite** for build tooling
- **React Router v6** for navigation
- **Tailwind CSS** for styling
- **Recharts** for data visualization
- **MSW** for API mocking
- **JWT Decode** for token handling

## Getting Started

### Prerequisites

- Node.js 16+ 
- npm or yarn

### Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm run dev
   ```

4. Open [http://localhost:5173](http://localhost:5173) in your browser

## Demo Credentials

### Admin User
- **Email**: `admin@demo.com`
- **Password**: `password123`
- **Access**: Admin dashboard with user management

### Regular User
- **Email**: `user@demo.com`
- **Password**: `password123`
- **Access**: User dashboard with activity charts

## Project Structure

```
src/
├── components/
│   ├── Layout.tsx          # Main layout wrapper
│   ├── Navbar.tsx          # Navigation bar with logout
│   └── PrivateRoute.tsx    # Route protection component
├── contexts/
│   └── AuthContext.tsx     # Authentication state management
├── pages/
│   ├── Login.tsx           # Login form
│   ├── UserDashboard.tsx   # User dashboard with charts
│   └── AdminDashboard.tsx  # Admin dashboard with user list
├── mocks/
│   ├── handlers.ts         # MSW API handlers
│   └── browser.ts          # MSW browser setup
├── types/
│   └── index.ts            # TypeScript type definitions
├── utils/
│   └── auth.ts             # Authentication utilities
├── App.tsx                 # Main app component with routing
└── main.tsx                # Application entry point
```

## Features Overview

### Authentication System
- JWT token-based authentication
- Role-based access control (admin/user)
- Persistent login sessions
- Automatic token validation

### User Dashboard
- **Daily Activity Chart**: Line chart showing visits and actions over time
- **Action Categories**: Bar chart displaying actions by category
- **Statistics Cards**: Summary metrics for total visits, actions, and averages

### Admin Dashboard
- **User Management**: Complete list of all users
- **User Statistics**: Cards showing total, active, inactive, and admin users
- **User Details**: Name, email, role, status, and last login information

### Mock API Endpoints
- `POST /api/auth/login` - User authentication
- `GET /api/auth/me` - Get current user info
- `GET /api/user/activity` - Get user activity data
- `GET /api/admin/users` - Get all users (admin only)

## Development

### Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint

### Adding New Features

1. **New Pages**: Add components to `src/pages/`
2. **API Endpoints**: Add handlers to `src/mocks/handlers.ts`
3. **Types**: Update `src/types/index.ts`
4. **Routes**: Update `src/App.tsx`

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## License

MIT License - feel free to use this project for learning and development purposes.