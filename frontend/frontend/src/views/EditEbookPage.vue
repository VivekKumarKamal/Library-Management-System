<template>
  <div class="container mt-5">
    <h1 class="mb-4">Edit Book</h1>
    <form @submit.prevent="updateBook" v-if="book">
      <div class="mb-3">
        <label for="bookTitle" class="form-label">Book Title</label>
        <input
          type="text"
          class="form-control"
          id="bookTitle"
          v-model="book.title"
          required
        />
      </div>
      <div class="mb-3">
        <label for="bookAuthors" class="form-label">Authors</label>
        <input
          type="text"
          class="form-control"
          id="bookAuthors"
          v-model="book.authors"
          required
        />
      </div>
      <div class="mb-3">
        <label for="bookContent" class="form-label">Book Content</label>
        <textarea
          class="form-control"
          id="bookContent"
          v-model="book.content"
          rows="5"
          required
        ></textarea>
      </div>
      <div class="mb-3">
        <label class="form-label">Sections (select at least one)</label>
        <div class="section-checkboxes">
          <div v-for="section in sections" :key="section.id" class="form-check">
            <input
              class="form-check-input"
              type="checkbox"
              :id="'section-' + section.id"
              :value="section.id"
              v-model="selectedSectionIds"
            />
            <label class="form-check-label" :for="'section-' + section.id">
              {{ section.name }}
            </label>
          </div>
        </div>
        <div v-if="showSectionError" class="text-danger mt-2">
          Please select at least one section.
        </div>
      </div>
      <button type="submit" class="btn btn-primary">Update Book</button>
    </form>
    <div v-else class="alert alert-warning" role="alert">
      Loading book details...
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "EditBook",
  props: ["id"],
  data() {
    return {
      book: null,
      sections: [],
      selectedSectionIds: [],
      showSectionError: false,
    };
  },
  created() {
    this.fetchBookDetails();
    this.fetchSections();
  },
  methods: {
    async fetchBookDetails() {
      try {
        const response = await axios.get(
          `http://localhost:5000/api/ebooks/${this.id}`,
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("access_token")}`,
            },
          }
        );
        this.book = response.data;
        this.selectedSectionIds = this.book.sections.map(
          (section) => section.id
        );
      } catch (error) {
        console.error("Error fetching book details:", error);
      }
    },
    async fetchSections() {
      try {
        const response = await axios.get("http://localhost:5000/api/sections", {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("access_token")}`,
          },
        });
        this.sections = response.data;
      } catch (error) {
        console.error("Error fetching sections:", error);
      }
    },
    async updateBook() {
      if (this.selectedSectionIds.length === 0) {
        this.showSectionError = true;
        return;
      }
      this.showSectionError = false;

      try {
        const response = await axios.put(
          `http://localhost:5000/api/ebooks/${this.id}`,
          {
            title: this.book.title,
            authors: this.book.authors,
            content: this.book.content,
            section_ids: this.selectedSectionIds,
          },
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("access_token")}`,
            },
          }
        );

        if (response.status === 200) {
          alert("Book updated successfully!");
          this.$router.push("/");
        }
      } catch (error) {
        console.error("Error updating book:", error);
        if (
          error.response &&
          error.response.data &&
          error.response.data.message
        ) {
          alert(error.response.data.message);
        } else {
          alert("Failed to update book. Please try again.");
        }
      }
    },
  },
};
</script>

<style scoped>
.container {
  max-width: 600px;
}

.form-check {
  padding: 0.5rem;
  margin-bottom: 0.5rem;
}

.form-check-input {
  margin-top: 0.3rem;
}
</style>
