<template>
  <div class="container mt-5">
    <h2 class="mb-4">Search Results</h2>
    <div class="row row-cols-1 row-cols-md-3 g-4">
      <div class="col" v-for="book in searchResults" :key="book.id">
        <div class="card h-100 shadow-sm">
          <div class="card-body">
            <h5 class="card-title">
              <router-link v-if="isLibrarian" :to="`/book/${book.id}`">{{ book.title }}</router-link>
              <span v-else>{{ book.title }}</span>
            </h5>
            <p class="card-text">by {{ book.authors }}</p>
            <p class="card-text">
              <small class="text-muted">Sections: {{ book.sections.map((s) => s.name).join(", ") }}</small>
            </p>
            <p class="card-text">
              <small class="text-muted">Released on: {{ formatDate(book.created_at) }}</small>
            </p>
            <p class="card-text">
              <small class="text-muted">
                Rating: {{ book.rating.toFixed(1) }} ({{ book.total_ratings }} ratings)
              </small>
            </p>
            <p class="card-text">
              <small class="text-muted">
                Total Borrows: {{ book.total_borrows }}
              </small>
            </p>
          </div>
          <div class="card-footer bg-transparent border-top-0">
            <template v-if="isLibrarian">
              <button class="btn btn-primary w-100 mb-2" @click="editBook(book.id)">
                Edit
              </button>
              <button class="btn btn-danger w-100" @click="deleteBook(book.id)">
                Delete
              </button>
            </template>
            <template v-else>
              <button class="btn btn-primary w-100" @click="borrowBook(book.id)">
                Borrow
              </button>
            </template>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "SearchPage",
  data() {
    return {
      searchResults: [],
      isLibrarian: false,
    };
  },
  created() {
    this.checkUserRole();
    this.performSearch();
  },
  methods: {
    async checkUserRole() {
      const token = localStorage.getItem("access_token");
      if (token) {
        try {
          const response = await axios.get(
            "http://localhost:5000/api/current-user",
            {
              headers: { Authorization: `Bearer ${token}` },
            }
          );
          this.isLibrarian = response.data.is_librarian;
        } catch (error) {
          console.error("Error fetching user role:", error);
          this.isLibrarian = false;
        }
      } else {
        this.isLibrarian = false;
      }
    },
    async performSearch() {
      const query = this.$route.query.q;
      if (query) {
        try {
          const response = await axios.get(`http://localhost:5000/api/search?q=${query}`, {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("access_token")}`,
            },
          });
          this.searchResults = response.data;
        } catch (error) {
          console.error("Error performing search:", error);
        }
      }
    },
    formatDate(dateString) {
      const date = new Date(dateString);
      return date.toLocaleDateString("en-US", {
        year: "numeric",
        month: "long",
        day: "numeric",
      });
    },
    editBook(bookId) {
      this.$router.push(`/edit-book/${bookId}`);
    },
    async deleteBook(bookId) {
      if (confirm('Are you sure you want to delete this book?')) {
        try {
          await axios.delete(`http://localhost:5000/api/ebooks/${bookId}`, {
            headers: { Authorization: `Bearer ${localStorage.getItem('access_token')}` }
          });
          this.searchResults = this.searchResults.filter(book => book.id !== bookId);
          alert('Book deleted successfully');
        } catch (error) {
          console.error('Error deleting book:', error);
          alert('Failed to delete the book');
        }
      }
    },
    async borrowBook(bookId) {
      if (!this.$root.isLoggedIn) {
        this.$router.push("/login");
        return;
      }
      try {
        const response = await axios.post(
          `http://localhost:5000/api/requests`,
          { ebook_id: bookId },
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("access_token")}`,
            },
          }
        );
        alert(response.data.message || "Borrow request submitted successfully");
      } catch (error) {
        console.error("Error borrowing book:", error);
        if (error.response && error.response.data && error.response.data.message) {
          alert(error.response.data.message);
        } else {
          alert("An error occurred while borrowing the book");
        }
      }
    },
  },
};
</script>

<style scoped>
.card {
  transition: transform 0.2s;
}

.card:hover {
  transform: translateY(-5px);
}
</style>
