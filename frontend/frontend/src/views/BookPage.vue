<template>
  <div v-if="book" class="container-fluid mt-5">
    <div class="row">
      <!-- Book details on the left -->
      <div class="col-md-3">
        <div class="card">
          <img
            src="https://i.pinimg.com/originals/55/b1/b5/55b1b5dbf1488a572f8aa37b0388d321.jpg"
            alt="Book cover"
            class="card-img-top"
          />
          <div class="card-body">
            <h5 class="card-title">{{ book.title }}</h5>
            <p class="card-text">By {{ book.authors }}</p>
            <p class="card-text">
              <strong>Sections:</strong>
              {{ book.sections.map((s) => s.name).join(", ") }}
            </p>
            <p class="card-text">
              <strong>Added on:</strong> {{ formatDate(book.created_at) }}
            </p>
            <p class="card-text">
              <strong>Rating:</strong> {{ book.rating.toFixed(1) }} ({{ book.total_ratings }} ratings)
            </p>
            <p class="card-text">
              <strong>Total Borrows:</strong> {{ book.total_borrows }}
            </p>
          </div>
        </div>
      </div>

      <!-- Book content in the center -->
      <div class="col-md-9">
        <div class="card">
          <div class="card-header bg-primary text-white">
            <h2 class="mb-0">{{ book.title }}</h2>
          </div>
          <div class="card-body">
            <div class="book-content">
              {{ book.content }}
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Feedback section -->
    <div class="row mt-5">
      <div class="col-12">
        <h3>feedbacks</h3>
        <div v-if="feedbacks.length > 0">
          <div v-for="feedback in feedbacks" :key="feedback.id" class="card mb-3">
            <div class="card-body">
              <h5 class="card-title">Rating: {{ feedback.rating }} / 5</h5>
              <p class="card-text">{{ feedback.content }}</p>
              <p class="card-text"><small class="text-muted">{{ formatDate(feedback.created_at) }}</small></p>
            </div>
          </div>
        </div>
        <div v-else class="alert alert-info">
          No feedback available for this book yet.
        </div>
      </div>
    </div>
  </div>
  <div v-else class="container mt-5">
    <div class="alert alert-warning" role="alert">
      You don't have access to this book or the book doesn't exist.
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "BookPage",
  data() {
    return {
      book: null,
      feedbacks: [],
    };
  },
  created() {
    this.fetchBook();
    this.fetchFeedbacks();
  },
  methods: {
    async fetchBook() {
      try {
        const response = await axios.get(
          `http://localhost:5000/api/ebooks/${this.$route.params.id}`,
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("access_token")}`,
            },
          }
        );
        this.book = response.data;
      } catch (error) {
        console.error("Error fetching book:", error);
        this.book = null;
      }
    },
    async fetchFeedbacks() {
      try {
        const response = await axios.get(
          `http://localhost:5000/api/feedback/${this.$route.params.id}`,
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("access_token")}`,
            },
          }
        );
        this.feedbacks = response.data;
      } catch (error) {
        console.error("Error fetching feedbacks:", error);
        this.feedbacks = [];
      }
    },
    formatDate(dateString) {
      const options = { year: "numeric", month: "long", day: "numeric", hour: "2-digit", minute: "2-digit" };
      return new Date(dateString).toLocaleDateString(undefined, options);
    },
  },
};
</script>

<style scoped>
.book-content {
  max-height: 70vh;
  overflow-y: auto;
  padding: 15px;
  border: 1px solid #dee2e6;
  border-radius: 0.25rem;
  line-height: 1.6;
  font-size: 1.1rem;
}

.card {
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.card-img-top {
  object-fit: cover;
  height: 400px;
}
</style>