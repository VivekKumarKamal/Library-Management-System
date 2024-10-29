<template>
    <div class="container mt-5">
  
      <!-- Create Section and Add Book Buttons -->
      <div class="text-end mb-4" v-if="$root.isLoggedIn && isLibrarian">
        <button @click="createSection" class="btn btn-success me-2">
          Create New Section
        </button>
        <button @click="addBook" class="btn btn-info">Add New Book</button>
      </div>
  

      <!-- New Books Section -->
      <div class="section mb-5">
        <h2 class="section-title">New Arrivals</h2>
        <div class="row row-cols-1 row-cols-md-3 g-4">
          <div class="col" v-for="book in newBooks" :key="book.id">
            <div class="card h-100 shadow-sm">
              <div class="card-body">
                <h5 class="card-title">
                  <router-link v-if="isLibrarian" :to="`/book/${book.id}`">{{
                    book.title
                  }}</router-link>
                  <span v-else>{{ book.title }}</span>
                </h5>
                <p class="card-text">by {{ book.authors }}</p>
                <p class="card-text">
                  <small class="text-muted"
                    >Sections:
                    {{ book.sections.map((s) => s.name).join(", ") }}</small
                  >
                </p>
                <p class="card-text">
                  <small class="text-muted"
                    >Released on: {{ formatDate(book.created_at) }}</small
                  >
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
  
      <!-- Books by Sections -->
      <div v-for="section in sections" :key="section.id" class="section mb-5">
        <div class="d-flex justify-content-between align-items-center mb-3">
          <div>
            <h2 class="section-title mb-0">{{ section.name }}</h2>
            <p class="section-description">
              <strong>Description:</strong> {{ section.description }}
            </p>
          </div>
          <div v-if="isLibrarian">
            <router-link
              :to="'/edit-section/' + section.id"
              class="btn btn-sm btn-outline-primary me-2"
              >Edit Section</router-link
            >
            <button
              class="btn btn-sm btn-outline-danger"
              @click="deleteSection(section.id)"
            >
              Delete Section
            </button>
          </div>
        </div>
        <div class="row row-cols-1 row-cols-md-3 g-4">
          <div class="col" v-for="book in section.ebooks" :key="book.id">
            <div class="card h-100 shadow-sm">
              <div class="card-body">
                <h5 class="card-title">
                  <router-link v-if="isLibrarian" :to="`/book/${book.id}`">{{
                    book.title
                  }}</router-link>
                  <span v-else>{{ book.title }}</span>
                </h5>
                <p class="card-text">by {{ book.authors }}</p>
                <p class="card-text">
                  <small class="text-muted"
                    >Released on: {{ formatDate(book.created_at) }}</small
                  >
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
    </div>
  </template>
  
  <script>
  import axios from "axios";
  
  export default {
    name: "HomePage",
    data() {
      return {
        newBooks: [],
        sections: [],
        isLibrarian: false,
        isLoggedIn: false,
      };
    },
    created() {
      this.checkUserRole();
      this.fetchNewBooks();
      this.fetchBooksBySections();
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
      async fetchNewBooks() {
        try {
          const response = await axios.get("http://localhost:5000/api/ebooks");
          this.newBooks = response.data;
        } catch (error) {
          console.error("Error fetching new books:", error);
        }
      },
      async fetchBooksBySections() {
        try {
          const response = await axios.get("http://localhost:5000/api/sections");
          this.sections = response.data;
        } catch (error) {
          console.error("Error fetching books by sections:", error);
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
      formatDate(dateString) {
        const date = new Date(dateString);
        return date.toLocaleDateString("en-US", {
          year: "numeric",
          month: "long",
          day: "numeric",
        });
      },
      createSection() {
        this.$router.push("/add-section");
      },
      addBook() {
        this.$router.push("/add-book");
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
            this.newBooks = this.newBooks.filter(book => book.id !== bookId);
            this.sections.forEach(section => {
              section.ebooks = section.ebooks.filter(book => book.id !== bookId);
            });
            alert('Book deleted successfully');
          } catch (error) {
            console.error('Error deleting book:', error);
            alert('Failed to delete the book');
          }
        }
      },
      async deleteSection(sectionId) {
        if (confirm('Are you sure you want to delete this section?')) {
          try {
            await axios.delete(`http://localhost:5000/api/sections/${sectionId}`, {
              headers: { Authorization: `Bearer ${localStorage.getItem('access_token')}` }
            });
            this.sections = this.sections.filter(section => section.id !== sectionId);
            alert('Section deleted successfully');
          } catch (error) {
            console.error('Error deleting section:', error);
            alert('Failed to delete the section');
          }
        }
      },
    },
    watch: {
      $route() {
        this.checkUserRole();
        this.fetchNewBooks();
        this.fetchBooksBySections();
      },
    },
  };
  </script>
  
  <style scoped>
  .section-title {
    font-size: 1.5rem;
    margin-bottom: 1rem;
    border-bottom: 2px solid #007bff;
    padding-bottom: 0.5rem;
  }
  .card {
    transition: transform 0.2s;
  }
  .card:hover {
    transform: translateY(-5px);
  }
  .card-title {
    font-weight: bold;
  }
  .btn-primary {
    background-color: #007bff;
    border-color: #007bff;
  }
  .btn-primary:hover {
    background-color: #0056b3;
    border-color: #0056b3;
  }
  .section-description {
    font-size: 0.9rem;
    color: #6c757d;
    margin-bottom: 1rem;
  }
  </style>