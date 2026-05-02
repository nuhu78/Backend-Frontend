import { Navigate, NavLink, Outlet, useLocation, useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

const navLinkClass = ({ isActive }) => `nav-link${isActive ? ' active' : ''}`

export function ProtectedRoute({ children, allowedRoles }) {
  const { isAuthenticated, loading, user } = useAuth()
  const location = useLocation()

  if (loading) {
    return <div className="page-loader">Loading dashboard...</div>
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" replace state={{ from: location.pathname }} />
  }

  if (allowedRoles?.length && user?.role && !allowedRoles.includes(user.role)) {
    return <Navigate to="/dashboard" replace />
  }

  return children
}

export function AppShell() {
  const { user, signOut } = useAuth()
  const navigate = useNavigate()

  const handleLogout = async () => {
    await signOut()
    navigate('/login', { replace: true })
  }

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div>
          <div className="brand-badge">LMS</div>
          <h2>Learning Command Center</h2>
          <p>Role-aware dashboard for students, instructors, and admins.</p>
        </div>

        <nav className="sidebar-nav">
          <NavLink to="/dashboard" className={navLinkClass} end>
            Dashboard
          </NavLink>
          <NavLink to="/courses" className={navLinkClass}>
            Courses
          </NavLink>
          <NavLink to="/profile" className={navLinkClass}>
            Profile
          </NavLink>
          {user?.role === 'ADMIN' ? (
            <NavLink to="/admin/users" className={navLinkClass}>
              Users & Reports
            </NavLink>
          ) : null}
        </nav>

        <button type="button" className="ghost-button sidebar-logout" onClick={handleLogout}>
          Logout
        </button>
      </aside>

      <main className="content-area">
        <header className="topbar">
          <div>
            <span className="eyebrow">Current role</span>
            <h1>{user?.role || 'Member'}</h1>
          </div>
          <div className="user-chip">
            <span>{user?.username}</span>
            <strong>{user?.role}</strong>
          </div>
        </header>

        <section className="content-card">
          <Outlet />
        </section>
      </main>
    </div>
  )
}
