import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './contexts/AuthContext';
import { PrivateRoute } from './components/PrivateRoute';
import { Layout } from './components/Layout';
import { Login } from './pages/Login';
import { UserDashboard } from './pages/UserDashboard';
import { AdminDashboard } from './pages/AdminDashboard';

function App() {
  return (
    <AuthProvider>
      <Router>
        <div className="App">
          <Routes>
            {/* Public route */}
            <Route path="/" element={<Login />} />
            
            {/* Protected routes */}
            <Route 
              path="/user" 
              element={
                <PrivateRoute requiredRole="user">
                  <Layout>
                    <UserDashboard />
                  </Layout>
                </PrivateRoute>
              } 
            />
            
            <Route 
              path="/admin" 
              element={
                <PrivateRoute requiredRole="admin">
                  <Layout>
                    <AdminDashboard />
                  </Layout>
                </PrivateRoute>
              } 
            />
            
            {/* Catch all route */}
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </div>
      </Router>
    </AuthProvider>
  );
}

export default App;



