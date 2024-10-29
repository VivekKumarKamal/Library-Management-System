<template>
  <div class="container mt-5">
    <h1 class="mb-4">Edit Profile</h1>
    <form @submit.prevent="updateProfile">
      <div class="mb-3">
        <label for="name" class="form-label">Name</label>
        <input
          type="text"
          class="form-control"
          id="name"
          v-model="name"
          required
        />
      </div>
      <div class="mb-3">
        <label for="email" class="form-label">Email</label>
        <input
          type="email"
          class="form-control"
          id="email"
          v-model="email"
          disabled
        />
      </div>
      <div class="mb-3">
        <label for="newPassword" class="form-label">New Password (leave blank if unchanged)</label>
        <input
          type="password"
          class="form-control"
          id="newPassword"
          v-model="newPassword"
        />
      </div>
      <div class="mb-3">
        <label for="confirmPassword" class="form-label">Confirm New Password</label>
        <input
          type="password"
          class="form-control"
          id="confirmPassword"
          v-model="confirmPassword"
        />
      </div>
      <button type="submit" class="btn btn-primary">Update Profile</button>
    </form>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "EditProfilePage",
  data() {
    return {
      name: "",
      email: "",
      newPassword: "",
      confirmPassword: "",
    };
  },
  created() {
    this.fetchUserProfile();
  },
  methods: {
    async fetchUserProfile() {
      try {
        const response = await axios.get("http://localhost:5000/api/user/profile", {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("access_token")}`,
          },
        });
        this.name = response.data.name;
        this.email = response.data.email;
      } catch (error) {
        console.error("Error fetching user profile:", error);
        alert("Failed to fetch user profile. Please try again.");
      }
    },
    async updateProfile() {
      if (this.newPassword !== this.confirmPassword) {
        alert("New password and confirm password do not match.");
        return;
      }

      try {
        const updateData = {
          name: this.name,
        };

        if (this.newPassword) {
          updateData.password = this.newPassword;
        }

        const response = await axios.put(
          "http://localhost:5000/api/user/profile",
          updateData,
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("access_token")}`,
            },
          }
        );

        if (response.status === 200) {
          alert("Profile updated successfully!");
          this.$router.push("/");
        }
      } catch (error) {
        console.error("Error updating profile:", error);
        if (error.response && error.response.data && error.response.data.message) {
          alert(error.response.data.message);
        } else {
          alert("Failed to update profile. Please try again.");
        }
      }
    },
  },
};
</script>

<style scoped>
.container {
  max-width: 500px;
}
</style>