<template>
  <div class="container mt-5">
    <div class="user-info mb-4">
      <h2>Welcome, {{ userName }}</h2>
      <p>Email: {{ userEmail }}</p>
      <button class="btn btn-secondary" @click="editProfile">Edit Profile</button>
    </div>

    <!-- Requested Books Table -->
    <div class="card mb-4">
      <div class="card-header bg-warning text-white">Requested Books</div>
      <div class="card-body p-0">
        <table class="table table-striped">
          <thead class="thead-dark">
            <tr>
              <th>Book Title</th>
              <th>Author</th>
              <th>Request Date</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="book in requestedBooks" :key="book.id">
              <td>
                {{ book.ebook_title }}
              </td>
              <td>{{ book.ebook_author }}</td>
              <td>{{ formatDate(book.request_date) }}</td>
            </tr>
            <tr v-if="requestedBooks.length === 0">
              <td colspan="3" class="text-center">No requested books found.</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Currently Reading Books Table -->
    <div class="card mb-4">
      <div class="card-header bg-success text-white">Currently Reading</div>
      <div class="card-body p-0">
        <table class="table table-striped">
          <thead class="thead-dark">
            <tr>
              <th>Book Title</th>
              <th>Author</th>
              <th>Date Issued</th>
              <th>Due Date</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="book in currentlyReadingBooks" :key="book.id">
              <td>
                <a :href="`/book/${book.ebook_id}`">{{ book.ebook_title }}</a>
              </td>
              <td>{{ book.ebook_author }}</td>
              <td>{{ formatDate(book.issue_date) }}</td>
              <td>{{ formatDate(book.due_date) }}</td>
              <td>
                <button
                  class="btn btn-danger btn-sm"
                  @click="returnBook(book.id)"
                >
                  Return Book
                </button>
              </td>
            </tr>
            <tr v-if="currentlyReadingBooks.length === 0">
              <td colspan="5" class="text-center">
                No books currently being read.
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Returned Books Table -->
    <div class="card">
      <div class="card-header bg-info text-white">Returned Books</div>
      <div class="card-body p-0">
        <table class="table table-striped">
          <thead class="thead-dark">
            <tr>
              <th>Book Title</th>
              <th>Author</th>
              <th>Date Returned</th>
              <th>Rating</th>
              <th>Feedback</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="book in ReturnedBooks" :key="book.id">
              <td>{{ book.ebook_title }}</td>
              <td>{{ book.ebook_author }}</td>
              <td>{{ formatDate(book.return_date) }}</td>
              <td>
                <template v-if="book.feedbackSubmitted">
                  {{ book.rating }}
                </template>
                <select v-else v-model="book.rating">
                  <option v-for="n in 5" :key="n" :value="n">{{ n }}</option>
                </select>
              </td>
              <td>
                <template v-if="book.feedbackSubmitted">
                  {{ book.feedback }}
                </template>
                <textarea v-else v-model="book.feedback"></textarea>
              </td>
              <td>
                <button
                  v-if="!book.feedbackSubmitted"
                  class="btn btn-primary btn-sm"
                  @click="submitFeedback(book)"
                >
                  Submit
                </button>
                <span v-else>Feedback submitted</span>
              </td>
            </tr>
            <tr v-if="ReturnedBooks.length === 0">
              <td colspan="6" class="text-center">
                No returned books found.
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      requestedBooks: [],
      currentlyReadingBooks: [],
      ReturnedBooks: [],
      userFeedbacks: {},
      userName: "",
      userEmail: "",
    };
  },
  created() {
    this.fetchUserProfile();
    this.fetchUserFeedbacks().then(() => {
      this.fetchRequestedBooks();
      this.fetchCurrentlyReadingBooks();
      this.fetchReturnedBooks();
    });
  },
  methods: {
    fetchRequestedBooks() {
      axios
        .get("http://localhost:5000/api/user/requests", {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("access_token")}`,
          },
        })
        .then((response) => {
          this.requestedBooks = response.data.filter(book => book.status === 'pending');
          console.log("Requested books:", this.requestedBooks); // Add this line for debugging
        })
        .catch((error) => {
          console.error("Error fetching requested books:", error);
        });
    },
    fetchCurrentlyReadingBooks() {
      axios
        .get("http://localhost:5000/api/user/requests", {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("access_token")}`,
          },
        })
        .then((response) => {
          this.currentlyReadingBooks = response.data.filter(book => book.status === 'granted');
          console.log("Currently reading books:", this.currentlyReadingBooks); // Add this line for debugging
        })
        .catch((error) => {
          console.error("Error fetching currently reading books:", error);
        });
    },
    fetchReturnedBooks() {
      axios
        .get("http://localhost:5000/api/returned-books", {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("access_token")}`,
          },
        })
        .then((response) => {
          console.log("Raw returned books data:", response.data);
          this.ReturnedBooks = response.data.map(book => ({
            ...book,
            rating: this.userFeedbacks[book.ebook_id]?.rating || 0,
            feedback: this.userFeedbacks[book.ebook_id]?.content || '',
            feedbackSubmitted: !!this.userFeedbacks[book.ebook_id]
          }));
          console.log("Returned books:", this.ReturnedBooks);
        })
        .catch((error) => {
          console.error("Error fetching returned books:", error);
        });
    },
    fetchUserFeedbacks() {
      return axios
        .get("http://localhost:5000/api/user/feedbacks", {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("access_token")}`,
          },
        })
        .then((response) => {
          this.userFeedbacks = response.data.reduce((acc, feedback) => {
            acc[feedback.ebook_id] = feedback;
            return acc;
          }, {});
          console.log("User feedbacks:", this.userFeedbacks);
        })
        .catch((error) => {
          console.error("Error fetching user feedbacks:", error);
        });
    },
    async fetchUserProfile() {
      try {
        const response = await axios.get("http://localhost:5000/api/user/profile", {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("access_token")}`,
          },
        });
        this.userName = response.data.name;
        this.userEmail = response.data.email;
      } catch (error) {
        console.error("Error fetching user profile:", error);
      }
    },
    returnBook(requestId) {
      axios
        .post(
          `http://localhost:5000/api/return-book/${requestId}`,
          {},
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("access_token")}`,
            },
          }
        )
        .then(() => {
          alert("Book returned successfully");
          this.fetchCurrentlyReadingBooks();
          this.fetchReturnedBooks();
        })
        .catch((error) => {
          console.error("Error returning book:", error);
          alert("Error returning book: " + error.response?.data?.message || "Unknown error");
        });
    },
    submitFeedback(book) {
      axios
        .post(
          `http://localhost:5000/api/feedback`,
          {
            ebook_id: book.ebook_id,
            rating: book.rating,
            content: book.feedback
          },
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("access_token")}`,
            },
          }
        )
        .then(() => {
          book.feedbackSubmitted = true;
          alert("Feedback submitted successfully");
        })
        .catch((error) => {
          console.error("Error submitting feedback:", error);
          alert("Error submitting feedback: " + error.response?.data?.message || "Unknown error");
        });
    },
    requestBook(bookId) {
      axios
        .post(
          `http://localhost:5000/api/request-book/${bookId}`,
          {},
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("access_token")}`,
            },
          }
        )
        .then(() => {
          alert("Book requested successfully");
          this.fetchRequestedBooks();
        })
        .catch((error) => {
          console.error("Error requesting book:", error);
        });
    },
    editProfile() {
      this.$router.push("/edit-profile");
    },
    formatDate(dateString) {
      if (!dateString) return 'N/A';
      const date = new Date(dateString);
      return date.toLocaleDateString();
    },
  },
};
</script>

<style scoped>
/* ... (styles remain unchanged) ... */
</style>