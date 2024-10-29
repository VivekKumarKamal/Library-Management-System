<template>
  <!-- Bootswatch -->
  <link
    rel="stylesheet"
    href="https://cdn.jsdelivr.net/npm/bootswatch@4.5.2/dist/sketchy/bootstrap.min.css"
    integrity="sha384-RxqHG2ilm4r6aFRpGmBbGTjsqwfqHOKy1ArsMhHusnRO47jcGqpIQqlQK/kmGy9R"
    crossorigin="anonymous"
  />
  <div id="app">
    <nav class="navbar navbar-expand-lg navbar-light bg-light mb-3">
      <div class="container-fluid">
        <router-link class="navbar-brand" to="/">LibraryApp</router-link>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
          <ul class="navbar-nav me-auto mb-2 mb-lg-0">
            <li class="nav-item">
              <router-link class="nav-link" to="/">Home</router-link>
            </li>
          </ul>
          <form class="d-flex" @submit.prevent="performSearch">
            <input class="form-control me-2" type="search" v-model="searchQuery" placeholder="Search books" aria-label="Search">
            <button class="btn btn-outline-success" type="submit">Search</button>
          </form>
          <ul class="navbar-nav">
            <li v-if="!isLoggedIn" class="nav-item">
              <router-link class="nav-link" to="/login">Login</router-link>
            </li>
            <li v-if="!isLoggedIn" class="nav-item">
              <router-link class="nav-link" to="/register">Register</router-link>
            </li>
            <li v-if="isLoggedIn && !isLibrarian" class="nav-item">
              <router-link class="nav-link" to="/user-dashboard"><i>{{ user?.name || 'User' }}'s Dashboard</i></router-link>
            </li>
            <li v-if="isLoggedIn && isLibrarian" class="nav-item">
              <router-link class="nav-link" to="/librarian-dashboard"><i>Librarian Dashboard</i></router-link>
            </li>
            <li v-if="isLoggedIn" class="nav-item">
              <button class="btn btn-outline-danger" @click="logout">Logout</button>
            </li>
          </ul>
        </div>
      </div>
    </nav>
    <div class="container mt-4">
      <router-view />
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { getCurrentUser } from '@/auth';

export default {
  data() {
    return {
      user: null,
      error: null,
      searchQuery: '',
    };
  },
  computed: {
    isLoggedIn() {
      return this.user !== null;
    },
    isLibrarian() {
      return this.user && this.user.is_librarian;
    },
  },
  methods: {
    logout() {
      localStorage.removeItem("access_token");
      localStorage.removeItem("user");
      this.user = null;
      this.$router.push("/");
    },
    async fetchCurrentUser() {
      this.user = await getCurrentUser();
      if (this.user) {
        const response = await axios.get("http://localhost:5000/api/user/profile", {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("access_token")}`,
          },
        });
        this.user.name = response.data.name;
      }
    },
    performSearch() {
      if (this.searchQuery.trim()) {
        this.$router.push({ name: 'search', query: { q: this.searchQuery.trim() } });
      }
    },
  },
  created() {
    this.fetchCurrentUser();
  },
  provide() {
    return {
      isLoggedIn: () => this.isLoggedIn,
      isLibrarian: () => this.isLibrarian,
      user: () => this.user,
    };
  },
};
</script>

<style>
#app {
  font-family: 'Comic Sans MS', cursive;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
}

h1 {
  font-size: 2.5rem;
  margin: 20px 0;
  text-align: center;
}

.navbar {
  margin-bottom: 20px;
}

.navbar-brand {
  font-size: 1.5rem;
  font-weight: bold;
}

.nav-link {
  font-size: 1.1rem;
}

.navbar-nav .nav-link.router-link-exact-active {
  color: #42b983;
  font-weight: bold;
}

.btn-outline-danger {
  border-width: 2px;
}

.container {
  background-color: #f8f9fa;
  border-radius: 15px;
  padding: 20px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}
</style>