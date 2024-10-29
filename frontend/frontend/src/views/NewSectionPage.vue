<template>
  <div class="container mt-5">
    <h1 class="mb-4">Create New Section</h1>
    <form @submit.prevent="createSection">
      <div class="mb-3">
        <label for="sectionName" class="form-label">Section Name</label>
        <input
          type="text"
          class="form-control"
          id="sectionName"
          v-model="sectionName"
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
          v-model="sectionDescription"
          rows="3"
          required
        ></textarea>
      </div>
      <button type="submit" class="btn btn-primary">Create Section</button>
    </form>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "NewSectionPage",
  data() {
    return {
      sectionName: "",
      sectionDescription: "",
    };
  },
  methods: {
    async createSection() {
      try {
        const response = await axios.post(
          "http://localhost:5000/api/sections",
          {
            name: this.sectionName,
            description: this.sectionDescription,
          },
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("access_token")}`,
            },
          }
        );

        if (response.status === 201) {
          alert("Section created successfully!");
          this.$router.push("/");
        }
      } catch (error) {
        console.error("Error creating section:", error);
        alert("Failed to create section. Please try again.");
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
