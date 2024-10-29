<template>
  <div class="container mt-4">
    <div class="user-info mb-4">
      <h2>Welcome, {{ userName }}</h2>
      <p>Email: {{ userEmail }}</p>
      <button class="btn btn-secondary" @click="editProfile">Edit Profile</button>
    </div>
    <h1 class="mb-4">Librarian Dashboard</h1>

    <!-- Statistics Cards -->
    <div class="row mb-4">
      <div class="col-md-3">
        <div class="card text-white bg-primary mb-3">
          <div class="card-body">
            <h5 class="card-title">Active Users</h5>
            <p class="card-text">{{ activeUsers }}</p>
          </div>
        </div>
      </div>
      <div class="col-md-3">
        <div class="card text-white bg-warning mb-3">
          <div class="card-body">
            <h5 class="card-title">Grant Requests</h5>
            <p class="card-text">{{ pendingRequests }}</p>
          </div>
        </div>
      </div>
      <div class="col-md-3">
        <div class="card text-white bg-success mb-3">
          <div class="card-body">
            <h5 class="card-title">E-books Issued</h5>
            <p class="card-text">{{ ebooksIssued }}</p>
          </div>
        </div>
      </div>
      <div class="col-md-3">
        <div class="card text-white bg-danger mb-3">
          <div class="card-body">
            <h5 class="card-title">E-books Revoked</h5>
            <p class="card-text">{{ ebooksRevoked }}</p>
          </div>
        </div>
      </div>
    </div>

    <!-- User Requests -->
    <div class="card mb-4">
      <div class="card-header">User Requests</div>
      <div class="card-body">
        <table class="table table-striped">
          <thead>
            <tr>
              <th>Request ID</th>
              <th>User</th>
              <th>E-book</th>
              <th>Author</th>
              <th>Request Date</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="request in userRequests" :key="request.id">
              <td>{{ request.id }}</td>
              <td>{{ request.user_name }}</td>
              <td>{{ request.ebook_title }}</td>
              <td>{{ request.ebook_author }}</td>
              <td>{{ formatDate(request.request_date) }}</td>
              <td>{{ request.status }}</td>
              <td>
                <button
                  v-if="request.status === 'pending'"
                  class="btn btn-sm btn-success mr-2"
                  @click="grantAccess(request)"
                >
                  Grant
                </button>
                <button
                  v-if="request.status === 'granted'"
                  class="btn btn-sm btn-warning mr-2"
                  @click="returnAccess(request)"
                >
                  Return
                </button>
                <button
                  v-if="request.status === 'pending'"
                  class="btn btn-sm btn-danger"
                  @click="revokeAccess(request)"
                >
                  Revoke
                </button>
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
      activeUsers: 0,
      pendingRequests: 0,
      ebooksIssued: 0,
      ebooksRevoked: 0,
      userRequests: [],
      userName: "",
      userEmail: "",
    };
  },
  methods: {
    async fetchStatistics() {
      try {
        const response = await axios.get(
          "http://localhost:5000/api/statistics",
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("access_token")}`,
            },
          }
        );
        this.activeUsers = response.data.activeUsers;
        this.pendingRequests = response.data.pendingRequests;
        this.ebooksIssued = response.data.ebooksIssued;
        this.ebooksRevoked = response.data.ebooksRevoked;
      } catch (error) {
        console.error("Error fetching statistics:", error);
      }
    },
    async fetchUserRequests() {
      try {
        const response = await axios.get("http://localhost:5000/api/requests", {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("access_token")}`,
          },
        });
        this.userRequests = response.data;
        console.log("User requests:", this.userRequests); // Add this line for debugging
      } catch (error) {
        console.error("Error fetching user requests:", error);
      }
    },
    async grantAccess(request) {
      try {
        await axios.put(
          `http://localhost:5000/api/requests/${request.id}`,
          { status: "granted" },
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("access_token")}`,
            },
          }
        );
        await this.fetchUserRequests();
        await this.fetchStatistics();
        alert("Access granted successfully");
      } catch (error) {
        console.error(
          "Error granting access:",
          error.response?.data || error.message
        );
        alert("Error granting access");
      }
    },
    async returnAccess(request) {
      try {
        await axios.put(
          `http://localhost:5000/api/requests/${request.id}`,
          { status: "returned" },
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("access_token")}`,
            },
          }
        );
        await this.fetchUserRequests();
        await this.fetchStatistics();
        alert("Book returned successfully");
      } catch (error) {
        console.error(
          "Error returning access:",
          error.response?.data || error.message
        );
        alert("Error returning book");
      }
    },
    async revokeAccess(request) {
      try {
        await axios.put(
          `http://localhost:5000/api/requests/${request.id}`,
          { status: "revoked" },
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("access_token")}`,
            },
          }
        );
        await this.fetchUserRequests();
        await this.fetchStatistics();
        alert("Access revoked successfully");
      } catch (error) {
        console.error(
          "Error revoking access:",
          error.response?.data || error.message
        );
        alert("Error revoking access");
      }
    },
    formatDate(dateString) {
      const options = {
        year: "numeric",
        month: "long",
        day: "numeric",
        hour: "2-digit",
        minute: "2-digit",
      };
      return new Date(dateString).toLocaleDateString(undefined, options);
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
  },
  created() {
    this.fetchStatistics();
    this.fetchUserRequests();
    this.fetchUserProfile();
  },
};
</script>

<style scoped>
.container {
  max-width: 1200px;
}
.card-header {
  background-color: #f8f9fa;
}
</style>