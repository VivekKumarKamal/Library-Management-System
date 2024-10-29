import axios from 'axios';

export async function getCurrentUser() {
  const token = localStorage.getItem('access_token');
  if (!token) return null;

  try {
    const response = await axios.get('http://localhost:5000/api/current-user', {
      headers: { Authorization: `Bearer ${token}` }
    });
    return response.data;
  } catch (error) {
    console.error('Error fetching current user:', error);
    return null;
  }
}

export function requiresUser(to, from, next) {
  getCurrentUser().then(user => {
    if (user && !user.is_librarian) {
      next(); // allow regular users
    } else {
      next('/'); // redirect librarians or non-authenticated users to home page
    }
  });
}

export function requiresLibrarian(to, from, next) {
  getCurrentUser().then(user => {
    if (user && user.is_librarian) {
      next(); // allow librarians
    } else {
      next('/'); // redirect regular users or non-authenticated users to home page
    }
  });
}
