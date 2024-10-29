<template>
  <div class="container mt-5">
    <h1 class="mb-4">Edit Section</h1>
    <form @submit.prevent="updateSection" v-if="section">
      <div class="mb-3">
        <label for="sectionName" class="form-label">Section Name</label>
        <input
          type="text"
          class="form-control"
          id="sectionName"
          v-model="section.name"
          required
        />
      </div>
      <div class="mb-3">
        <label for="sectionDescription" class="form-label"
          >Section Description</label
        >
        <textarea
          class="form-control"
          id="sectionDescription"
          v-model="section.description"
          rows="3"
          required
        ></textarea>
      </div>
      <button type="submit" class="btn btn-primary">Update Section</button>
    </form>
    <div v-else class="alert alert-warning" role="alert">
      Loading section details...
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "EditSectionPage",
  props: ["id"],
  data() {
    return {
      section: null,
    };
  },
  created() {
    this.fetchSectionDetails();
  },
  methods: {
    async fetchSectionDetails() {
      try {
        const response = await axios.get(
          `http://localhost:5000/api/sections/${this.id}`,
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("access_token")}`,
            },
          }
        );
        this.section = response.data;
      } catch (error) {
        console.error("Error fetching section details:", error);
        alert("Failed to fetch section details. Please try again.");
      }
    },
    async updateSection() {
      try {
        const response = await axios.put(
          `http://localhost:5000/api/sections/${this.id}`,
          {
            name: this.section.name,
            description: this.section.description,
          },
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("access_token")}`,
            },
          }
        );

        if (response.status === 200) {
          alert("Section updated successfully!");
          this.$router.push("/"); // Redirect to home page or sections list
        }
      } catch (error) {
        console.error("Error updating section:", error);
        if (
          error.response &&
          error.response.data &&
          error.response.data.message
        ) {
          alert(error.response.data.message);
        } else {
          alert("Failed to update section. Please try again.");
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
</style>
