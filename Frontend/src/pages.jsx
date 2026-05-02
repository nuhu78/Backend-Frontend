import { useEffect, useMemo, useState } from 'react'
import { Link, useParams } from 'react-router-dom'
import { useAuth } from './context/AuthContext'
import { apiRequest } from './lib/api'

function StatCard({ label, value, note }) {
  return (
    <article className="stat-card">
      <span>{label}</span>
      <strong>{value}</strong>
      <p>{note}</p>
    </article>
  )
}

export function LandingPage() {
  return (
    <div className="marketing-page">
      <section className="hero-panel">
        <div className="hero-copy">
          <span className="eyebrow">Full Stack LMS</span>
          <h1>Build, enroll, and manage learning with one secure workspace.</h1>
          <p>
            A React frontend for your Django LMS backend with role-based access,
            JWT auth, profile controls, course management, and admin reporting.
          </p>
          <div className="button-row">
            <Link className="primary-button" to="/login">
              Sign in
            </Link>
            <Link className="secondary-button" to="/register">
              Create account
            </Link>
          </div>
        </div>

        <div className="hero-grid">
          <article>
            <strong>JWT</strong>
            <span>Secure token-based login and refresh handling.</span>
          </article>
          <article>
            <strong>Roles</strong>
            <span>Admin, Instructor, and Student views with protected routes.</span>
          </article>
          <article>
            <strong>Reports</strong>
            <span>Dashboard summaries and user analytics in one place.</span>
          </article>
          <article>
            <strong>Courses</strong>
            <span>Browse, manage, enroll, and inspect course details.</span>
          </article>
        </div>
      </section>
    </div>
  )
}

export function LoginPage() {
  const [identifier, setIdentifier] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const { signIn } = useAuth()

  const handleSubmit = async (event) => {
    event.preventDefault()
    setError('')
    setLoading(true)

    try {
      await signIn({ identifier, password })
      window.location.href = '/dashboard'
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="auth-page">
      <form className="auth-card" onSubmit={handleSubmit}>
        <span className="eyebrow">Welcome back</span>
        <h1>Sign in</h1>
        <p>Use your username or phone number and password to continue.</p>

        <label>
          Username or phone
          <input value={identifier} onChange={(event) => setIdentifier(event.target.value)} />
        </label>

        <label>
          Password
          <input
            type="password"
            value={password}
            onChange={(event) => setPassword(event.target.value)}
          />
        </label>

        {error ? <div className="form-error">{error}</div> : null}

        <button type="submit" className="primary-button" disabled={loading}>
          {loading ? 'Signing in...' : 'Sign in'}
        </button>

        <div className="auth-links">
          <Link to="/forgot-password">Forgot password?</Link>
          <Link to="/register">Create a new account</Link>
        </div>
      </form>
    </div>
  )
}

export function RegisterPage() {
  const [form, setForm] = useState({
    username: '',
    email: '',
    password: '',
    role: 'STUDENT',
    phone: '',
  })
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const { signUp } = useAuth()

  const updateField = (field) => (event) => {
    setForm((current) => ({ ...current, [field]: event.target.value }))
  }

  const handleSubmit = async (event) => {
    event.preventDefault()
    setError('')
    setLoading(true)

    try {
      await signUp(form)
      window.location.href = '/dashboard'
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="auth-page">
      <form className="auth-card" onSubmit={handleSubmit}>
        <span className="eyebrow">Join the LMS</span>
        <h1>Create account</h1>
        <p>Register as a student or instructor and start using the secured API.</p>

        <label>
          Username
          <input value={form.username} onChange={updateField('username')} />
        </label>

        <label>
          Email
          <input type="email" value={form.email} onChange={updateField('email')} />
        </label>

        <label>
          Phone
          <input value={form.phone} onChange={updateField('phone')} />
        </label>

        <label>
          Password
          <input type="password" value={form.password} onChange={updateField('password')} />
        </label>

        <label>
          Role
          <select value={form.role} onChange={updateField('role')}>
            <option value="STUDENT">Student</option>
            <option value="INSTRUCTOR">Instructor</option>
          </select>
        </label>

        {error ? <div className="form-error">{error}</div> : null}

        <button type="submit" className="primary-button" disabled={loading}>
          {loading ? 'Creating account...' : 'Create account'}
        </button>

        <div className="auth-links">
          <Link to="/login">Already have an account?</Link>
        </div>
      </form>
    </div>
  )
}

export function ForgotPasswordPage() {
  const [email, setEmail] = useState('')
  const [message, setMessage] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const { forgotPassword } = useAuth()

  const handleSubmit = async (event) => {
    event.preventDefault()
    setLoading(true)
    setError('')
    setMessage('')

    try {
      const response = await forgotPassword(email)
      setMessage(response.message)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="auth-page">
      <form className="auth-card" onSubmit={handleSubmit}>
        <span className="eyebrow">Password help</span>
        <h1>Forgot password</h1>
        <p>Request a reset link to the email address on your account.</p>

        <label>
          Email
          <input type="email" value={email} onChange={(event) => setEmail(event.target.value)} />
        </label>

        {message ? <div className="form-success">{message}</div> : null}
        {error ? <div className="form-error">{error}</div> : null}

        <button type="submit" className="primary-button" disabled={loading}>
          {loading ? 'Sending...' : 'Send reset link'}
        </button>

        <div className="auth-links">
          <Link to="/login">Back to sign in</Link>
        </div>
      </form>
    </div>
  )
}

export function ResetPasswordPage() {
  const { uid, token } = useParams()
  const [password, setPassword] = useState('')
  const [message, setMessage] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const { resetPassword } = useAuth()

  const handleSubmit = async (event) => {
    event.preventDefault()
    setLoading(true)
    setError('')
    setMessage('')

    try {
      const response = await resetPassword({ uid, token, new_password: password })
      setMessage(response.message)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="auth-page">
      <form className="auth-card" onSubmit={handleSubmit}>
        <span className="eyebrow">New credentials</span>
        <h1>Reset password</h1>
        <p>Create a new password for your LMS account.</p>

        <label>
          New password
          <input type="password" value={password} onChange={(event) => setPassword(event.target.value)} />
        </label>

        {message ? <div className="form-success">{message}</div> : null}
        {error ? <div className="form-error">{error}</div> : null}

        <button type="submit" className="primary-button" disabled={loading}>
          {loading ? 'Updating...' : 'Reset password'}
        </button>

        <div className="auth-links">
          <Link to="/login">Back to sign in</Link>
        </div>
      </form>
    </div>
  )
}

export function DashboardPage() {
  const { user } = useAuth()
  const [summary, setSummary] = useState(null)
  const [recentCourses, setRecentCourses] = useState([])
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const load = async () => {
      setLoading(true)
      setError('')

      try {
        if (user?.role === 'ADMIN') {
          const data = await apiRequest('/dashboard/summary/')
          setSummary(data)
        } else {
          const [courses, enrollments] = await Promise.all([
            apiRequest('/courses/'),
            apiRequest('/enrollments/'),
          ])

          const courseList = courses.results || courses
          const enrollmentList = enrollments.results || enrollments

          setSummary({
            users_total: user ? 1 : 0,
            courses_total: courseList.length,
            enrollments_total: enrollmentList.length,
            published_courses: courseList.filter((course) => course.is_published).length,
            active_enrollments: enrollmentList.filter((enrollment) => enrollment.is_active).length,
            role_counts: null,
          })

          setRecentCourses(courseList.slice(0, 3))
        }
      } catch (err) {
        setError(err.message)
      } finally {
        setLoading(false)
      }
    }

    load()
  }, [user])

  if (loading) {
    return <div className="panel-empty">Loading summary...</div>
  }

  if (error) {
    return <div className="panel-empty error">{error}</div>
  }

  return (
    <div className="panel-stack">
      <section className="section-header">
        <div>
          <span className="eyebrow">Overview</span>
          <h2>Dashboard summary</h2>
          <p>Quick snapshot for {user?.role?.toLowerCase()}s with role-aware shortcuts.</p>
        </div>
        <Link to="/courses" className="secondary-button">
          Open courses
        </Link>
      </section>

      <div className="stats-grid">
        <StatCard label="Users" value={summary?.users_total ?? 0} note="Total registered users" />
        <StatCard label="Courses" value={summary?.courses_total ?? 0} note="Available course records" />
        <StatCard
          label="Enrollments"
          value={summary?.enrollments_total ?? 0}
          note="Active learning registrations"
        />
        <StatCard
          label="Published"
          value={summary?.published_courses ?? 0}
          note="Courses visible to students"
        />
      </div>

      {summary?.role_counts ? (
        <section className="detail-grid">
          <article className="detail-card">
            <h3>Role wise users</h3>
            <dl className="role-list">
              <div>
                <dt>Admins</dt>
                <dd>{summary.role_counts.ADMIN}</dd>
              </div>
              <div>
                <dt>Instructors</dt>
                <dd>{summary.role_counts.INSTRUCTOR}</dd>
              </div>
              <div>
                <dt>Students</dt>
                <dd>{summary.role_counts.STUDENT}</dd>
              </div>
            </dl>
          </article>

          <article className="detail-card">
            <h3>Active links</h3>
            <div className="button-stack">
              <Link to="/courses" className="ghost-button">
                Manage courses
              </Link>
              <Link to="/admin/users" className="ghost-button">
                View user report
              </Link>
              <Link to="/profile" className="ghost-button">
                Update profile
              </Link>
            </div>
          </article>
        </section>
      ) : null}

      {recentCourses.length ? (
        <section className="detail-card">
          <h3>Recent courses</h3>
          <div className="course-preview-list">
            {recentCourses.map((course) => (
              <article key={course.id} className="course-preview-item">
                <div>
                  <strong>{course.title}</strong>
                  <p>{course.category_name || 'Uncategorized'}</p>
                </div>
                <Link to={`/courses/${course.id}`}>Details</Link>
              </article>
            ))}
          </div>
        </section>
      ) : null}
    </div>
  )
}

export function CoursesPage() {
  const { user } = useAuth()
  const [courses, setCourses] = useState([])
  const [categories, setCategories] = useState([])
  const [form, setForm] = useState({
    title: '',
    description: '',
    category: '',
    level: 'BEGINNER',
    price: '0',
    is_published: true,
  })
  const [editingId, setEditingId] = useState(null)
  const [enrollmentBusy, setEnrollmentBusy] = useState(null)
  const [message, setMessage] = useState('')
  const [error, setError] = useState('')
  const canManage = user?.role === 'ADMIN' || user?.role === 'INSTRUCTOR'

  const loadData = async () => {
    try {
      const [courseData, categoryData] = await Promise.all([
        apiRequest('/courses/'),
        apiRequest('/categories/'),
      ])

      setCourses(courseData.results || courseData)
      setCategories(categoryData.results || categoryData)
    } catch (err) {
      setError(err.message)
    }
  }

  useEffect(() => {
    loadData()
  }, [])

  const sortedCourses = useMemo(
    () => [...courses].sort((left, right) => right.id - left.id),
    [courses],
  )

  const updateField = (field) => (event) => {
    const value = field === 'is_published' ? event.target.checked : event.target.value
    setForm((current) => ({ ...current, [field]: value }))
  }

  const startEdit = (course) => {
    setEditingId(course.id)
    setForm({
      title: course.title || '',
      description: course.description || '',
      category: course.category || '',
      level: course.level || 'BEGINNER',
      price: String(course.price ?? 0),
      is_published: Boolean(course.is_published),
    })
  }

  const clearForm = () => {
    setEditingId(null)
    setForm({
      title: '',
      description: '',
      category: '',
      level: 'BEGINNER',
      price: '0',
      is_published: true,
    })
  }

  const submitCourse = async (event) => {
    event.preventDefault()
    setError('')
    setMessage('')

    try {
      const payload = {
        ...form,
        category: form.category ? Number(form.category) : null,
        price: Number(form.price),
      }

      if (editingId) {
        await apiRequest(`/courses/${editingId}/`, {
          method: 'PUT',
          body: payload,
        })
        setMessage('Course updated successfully.')
      } else {
        await apiRequest('/courses/', {
          method: 'POST',
          body: payload,
        })
        setMessage('Course created successfully.')
      }

      clearForm()
      await loadData()
    } catch (err) {
      setError(err.message)
    }
  }

  const deleteCourse = async (courseId) => {
    if (!window.confirm('Delete this course?')) {
      return
    }

    try {
      await apiRequest(`/courses/${courseId}/`, { method: 'DELETE' })
      setMessage('Course deleted successfully.')
      await loadData()
    } catch (err) {
      setError(err.message)
    }
  }

  const enrollCourse = async (courseId) => {
    setEnrollmentBusy(courseId)
    setError('')
    setMessage('')

    try {
      await apiRequest('/enrollments/', {
        method: 'POST',
        body: { course: courseId },
      })
      setMessage('Enrollment completed successfully.')
    } catch (err) {
      setError(err.message)
    } finally {
      setEnrollmentBusy(null)
    }
  }

  return (
    <div className="panel-stack">
      <section className="section-header">
        <div>
          <span className="eyebrow">LMS Core</span>
          <h2>Courses</h2>
          <p>Browse course listings, manage them as an instructor, or enroll as a student.</p>
        </div>
      </section>

      {canManage ? (
        <form className="detail-card form-grid" onSubmit={submitCourse}>
          <h3 className="full-span">{editingId ? 'Edit course' : 'Create course'}</h3>

          <label>
            Title
            <input value={form.title} onChange={updateField('title')} />
          </label>

          <label className="full-span">
            Description
            <textarea rows="4" value={form.description} onChange={updateField('description')} />
          </label>

          <label>
            Category
            <select value={form.category} onChange={updateField('category')}>
              <option value="">Choose category</option>
              {categories.map((category) => (
                <option key={category.id} value={category.id}>
                  {category.name}
                </option>
              ))}
            </select>
          </label>

          <label>
            Level
            <select value={form.level} onChange={updateField('level')}>
              <option value="BEGINNER">Beginner</option>
              <option value="INTERMEDIATE">Intermediate</option>
              <option value="ADVANCED">Advanced</option>
            </select>
          </label>

          <label>
            Price
            <input type="number" min="0" step="0.01" value={form.price} onChange={updateField('price')} />
          </label>

          <label className="toggle-row">
            <input type="checkbox" checked={form.is_published} onChange={updateField('is_published')} />
            Published
          </label>

          <div className="button-row full-span">
            <button className="primary-button" type="submit">
              {editingId ? 'Update course' : 'Create course'}
            </button>
            {editingId ? (
              <button className="secondary-button" type="button" onClick={clearForm}>
                Cancel edit
              </button>
            ) : null}
          </div>
        </form>
      ) : null}

      {message ? <div className="form-success">{message}</div> : null}
      {error ? <div className="form-error">{error}</div> : null}

      <div className="course-grid">
        {sortedCourses.map((course) => (
          <article key={course.id} className="course-card">
            <div className="course-card__top">
              <span className="badge">{course.level}</span>
              <span className="course-price">${course.price}</span>
            </div>
            <h3>{course.title}</h3>
            <p>{course.description}</p>
            <div className="course-meta">
              <span>{course.category_name || 'No category'}</span>
              <span>{course.instructor_name || 'Instructor pending'}</span>
            </div>
            <div className="button-row">
              <Link to={`/courses/${course.id}`} className="ghost-button">
                Details
              </Link>
              {user?.role === 'STUDENT' ? (
                <button
                  type="button"
                  className="secondary-button"
                  disabled={enrollmentBusy === course.id}
                  onClick={() => enrollCourse(course.id)}
                >
                  {enrollmentBusy === course.id ? 'Enrolling...' : 'Enroll'}
                </button>
              ) : null}
              {canManage ? (
                <>
                  <button type="button" className="secondary-button" onClick={() => startEdit(course)}>
                    Edit
                  </button>
                  <button type="button" className="ghost-button danger" onClick={() => deleteCourse(course.id)}>
                    Delete
                  </button>
                </>
              ) : null}
            </div>
          </article>
        ))}
      </div>
    </div>
  )
}

export function CourseDetailsPage() {
  const { courseId } = useParams()
  const { user } = useAuth()
  const [course, setCourse] = useState(null)
  const [lessons, setLessons] = useState([])
  const [message, setMessage] = useState('')
  const [error, setError] = useState('')

  useEffect(() => {
    const load = async () => {
      try {
        const [courseData, lessonData] = await Promise.all([
          apiRequest(`/courses/${courseId}/`),
          apiRequest('/lessons/'),
        ])

        setCourse(courseData)
        const lessons = lessonData.results || lessonData
        setLessons(lessons.filter((lesson) => String(lesson.course) === String(courseId)))
      } catch (err) {
        setError(err.message)
      }
    }

    load()
  }, [courseId])

  const enroll = async () => {
    setError('')
    setMessage('')

    try {
      await apiRequest('/enrollments/', {
        method: 'POST',
        body: { course: Number(courseId) },
      })
      setMessage('Enrollment completed successfully.')
    } catch (err) {
      setError(err.message)
    }
  }

  if (!course && !error) {
    return <div className="panel-empty">Loading course...</div>
  }

  if (error) {
    return <div className="panel-empty error">{error}</div>
  }

  return (
    <div className="panel-stack">
      <div className="section-header">
        <div>
          <span className="eyebrow">Course profile</span>
          <h2>{course.title}</h2>
          <p>
            {course.category_name || 'Uncategorized'} · {course.level}
          </p>
        </div>
        <Link to="/courses" className="secondary-button">
          Back to courses
        </Link>
      </div>

      <section className="detail-grid">
        <article className="detail-card">
          <h3>About this course</h3>
          <p>{course.description}</p>
          <dl className="info-list">
            <div>
              <dt>Instructor</dt>
              <dd>{course.instructor_name || 'Not assigned yet'}</dd>
            </div>
            <div>
              <dt>Price</dt>
              <dd>${course.price}</dd>
            </div>
            <div>
              <dt>Status</dt>
              <dd>{course.is_published ? 'Published' : 'Draft'}</dd>
            </div>
          </dl>

          {user?.role === 'STUDENT' ? (
            <button type="button" className="primary-button" onClick={enroll}>
              Enroll now
            </button>
          ) : null}

          {message ? <div className="form-success">{message}</div> : null}
        </article>

        <article className="detail-card">
          <h3>Lessons</h3>
          {lessons.length ? (
            <div className="lesson-list">
              {lessons.map((lesson) => (
                <article key={lesson.id} className="lesson-item">
                  <strong>{lesson.title}</strong>
                  <p>{lesson.description}</p>
                </article>
              ))}
            </div>
          ) : (
            <p>No lessons attached yet.</p>
          )}
        </article>
      </section>
    </div>
  )
}

export function ProfilePage() {
  const { user, updateProfile, refreshProfile } = useAuth()
  const [form, setForm] = useState({
    username: '',
    first_name: '',
    last_name: '',
    email: '',
    phone: '',
    address: '',
    bio: '',
  })
  const [message, setMessage] = useState('')
  const [error, setError] = useState('')

  useEffect(() => {
    if (user) {
      setForm({
        username: user.username || '',
        first_name: user.first_name || '',
        last_name: user.last_name || '',
        email: user.email || '',
        phone: user.phone || '',
        address: user.address || '',
        bio: user.bio || '',
      })
    }
  }, [user])

  const updateField = (field) => (event) => {
    setForm((current) => ({ ...current, [field]: event.target.value }))
  }

  const handleSubmit = async (event) => {
    event.preventDefault()
    setMessage('')
    setError('')

    try {
      await updateProfile(form)
      await refreshProfile()
      setMessage('Profile updated successfully.')
    } catch (err) {
      setError(err.message)
    }
  }

  return (
    <div className="panel-stack">
      <section className="section-header">
        <div>
          <span className="eyebrow">Account</span>
          <h2>Profile</h2>
          <p>Update your contact details and role-specific profile data.</p>
        </div>
      </section>

      <form className="detail-card form-grid" onSubmit={handleSubmit}>
        <label>
          Username
          <input value={form.username} onChange={updateField('username')} />
        </label>
        <label>
          First name
          <input value={form.first_name} onChange={updateField('first_name')} />
        </label>
        <label>
          Last name
          <input value={form.last_name} onChange={updateField('last_name')} />
        </label>
        <label>
          Email
          <input type="email" value={form.email} onChange={updateField('email')} />
        </label>
        <label>
          Phone
          <input value={form.phone} onChange={updateField('phone')} />
        </label>
        <label className="full-span">
          Address
          <input value={form.address} onChange={updateField('address')} />
        </label>
        <label className="full-span">
          Bio
          <textarea rows="4" value={form.bio} onChange={updateField('bio')} />
        </label>

        <div className="button-row full-span">
          <button type="submit" className="primary-button">
            Save profile
          </button>
        </div>

        {message ? <div className="form-success full-span">{message}</div> : null}
        {error ? <div className="form-error full-span">{error}</div> : null}
      </form>
    </div>
  )
}

export function AdminUsersPage() {
  const [summary, setSummary] = useState(null)
  const [users, setUsers] = useState([])
  const [message, setMessage] = useState('')
  const [error, setError] = useState('')

  const load = async () => {
    try {
      const [summaryData, usersData] = await Promise.all([
        apiRequest('/admin/users/summary/'),
        apiRequest('/admin/users/'),
      ])

      setSummary(summaryData)
      setUsers(usersData.results || usersData)
    } catch (err) {
      setError(err.message)
    }
  }

  useEffect(() => {
    load()
  }, [])

  const toggleUser = async (user) => {
    setMessage('')
    setError('')

    try {
      await apiRequest(`/admin/users/${user.id}/`, {
        method: 'PUT',
        body: {
          username: user.username,
          email: user.email,
          first_name: user.first_name,
          last_name: user.last_name,
          is_active: !user.is_active,
          role: user.role,
        },
      })

      setMessage('User status updated successfully.')
      await load()
    } catch (err) {
      setError(err.message)
    }
  }

  return (
    <div className="panel-stack">
      <section className="section-header">
        <div>
          <span className="eyebrow">Administration</span>
          <h2>User summary</h2>
          <p>Admin-only reporting for account totals and role distribution.</p>
        </div>
      </section>

      {error ? <div className="form-error">{error}</div> : null}
      {message ? <div className="form-success">{message}</div> : null}

      <div className="stats-grid">
        <StatCard label="Users" value={summary?.total_users ?? 0} note="Registered accounts" />
        <StatCard label="Active" value={summary?.active_users ?? 0} note="Enabled accounts" />
        <StatCard label="Inactive" value={summary?.inactive_users ?? 0} note="Disabled accounts" />
        <StatCard label="Roles" value={Object.keys(summary?.role_counts || {}).length} note="Role groups" />
      </div>

      <section className="detail-card">
        <h3>Role counts</h3>
        <div className="role-bars">
          {summary?.role_counts ? (
            Object.entries(summary.role_counts).map(([role, count]) => (
              <div key={role} className="role-bar">
                <span>{role}</span>
                <strong>{count}</strong>
              </div>
            ))
          ) : (
            <p>No summary available.</p>
          )}
        </div>
      </section>

      <section className="detail-card">
        <h3>User table</h3>
        <div className="admin-table">
          {users.map((item) => (
            <article key={item.id} className="admin-row">
              <div>
                <strong>{item.username}</strong>
                <p>{item.email}</p>
              </div>
              <div>
                <span className="badge">{item.role}</span>
              </div>
              <div>
                <span>{item.is_active ? 'Active' : 'Inactive'}</span>
              </div>
              <button type="button" className="secondary-button" onClick={() => toggleUser(item)}>
                {item.is_active ? 'Deactivate' : 'Activate'}
              </button>
            </article>
          ))}
        </div>
      </section>
    </div>
  )
}
