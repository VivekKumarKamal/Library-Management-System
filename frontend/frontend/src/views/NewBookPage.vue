<template>
  <div class="container mt-5">
    <h1 class="mb-4">Add New Book</h1>
    <form @submit.prevent="addBook">
      <div class="mb-3">
        <label for="bookTitle" class="form-label">Book Title</label>
        <input
          type="text"
          class="form-control"
          id="bookTitle"
          v-model="bookTitle"
          required
        />
      </div>
      <div class="mb-3">
        <label for="bookAuthors" class="form-label">Authors</label>
        <input
          type="text"
          class="form-control"
          id="bookAuthors"
          v-model="bookAuthors"
          required
        />
      </div>
      <div class="mb-3">
        <label for="bookContent" class="form-label">Book Content</label>
        <textarea
          class="form-control"
          id="bookContent"
          v-model="bookContent"
          rows="5"
          required
        ></textarea>
      </div>
      <div class="mb-3">
        <label class="form-label">Sections (select at least one)</label>
        <br />
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
      <button type="submit" class="btn btn-primary">Add Book</button>
    </form>
  </div>
  <br /><br />
</template>

<script>
import axios from "axios";

export default {
  name: "NewBookPage",
  data() {
    return {
      bookTitle: "",
      bookAuthors: "",
      bookContent: "",
      selectedSectionIds: [],
      sections: [],
      showSectionError: false,
    };
  },
  created() {
    this.fetchSections();
  },
  methods: {
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
    async addBook() {
      if (this.selectedSectionIds.length === 0) {
        this.showSectionError = true;
        return;
      }
      this.showSectionError = false;

      try {
        const response = await axios.post(
          "http://localhost:5000/api/ebooks",
          {
            title: this.bookTitle,
            authors: this.bookAuthors,
            content: this.bookContent,
            section_ids: this.selectedSectionIds,
          },
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("access_token")}`,
            },
          }
        );

        if (response.status === 201) {
          alert("Book added successfully!");
          this.$router.push("/");
        }
      } catch (error) {
        console.error("Error adding book:", error);
        if (
          error.response &&
          error.response.data &&
          error.response.data.message
        ) {
          alert(error.response.data.message);
        } else {
          alert("Failed to add book. Please try again.");
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
