<template>
    <div class="container mt-5">
      <div class="row justify-content-center">
        <div class="col-md-6">
          <div class="card">
            <div class="card-header text-white bg-dark">
              <h3 class="text-center">Login</h3>
            </div>
            <div class="card-body">
              <form @submit.prevent="login">
                <div class="mb-3 row">
                  <label for="email" class="col-sm-4 col-form-label text-end"
                    >Email</label
                  >
                  <div class="col-sm-8">
                    <input
                      type="email"
                      class="form-control"
                      id="email"
                      v-model="email"
                      required
                    />
                  </div>
                </div>
                <div class="mb-3 row">
                  <label for="password" class="col-sm-4 col-form-label text-end"
                    >Password</label
                  >
                  <div class="col-sm-8">
                    <input
                      type="password"
                      class="form-control"
                      id="password"
                      v-model="password"
                      required
                    />
                  </div>
                </div>
                <button type="submit" class="btn btn-primary w-100">Login</button>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import axios from "axios";
  
  export default {
    name: "LoginPage",
    data() {
      return {
        email: "",
        password: "",
      };
    },
    methods: {
      async login() {
        try {
          const response = await axios.post("http://localhost:5000/login", {
            email: this.email,
            password: this.password,
          });
  
          console.log("Login response:", response.data);
  
          if (response.data.access_token) {
            localStorage.setItem("access_token", response.data.access_token);
            localStorage.setItem("user", JSON.stringify(response.data.user));
            this.$root.$emit("login", response.data.user);
            this.$router.push("/");
          } else {
            alert("Login failed. Please try again.");
          }
        } catch (error) {
          console.error("Login error:", error);
          if (
            error.response &&
            error.response.data &&
            error.response.data.message
          ) {
            alert(error.response.data.message);
          } else {
            alert("An error occurred during login. Please try again.");
          }
        }
      },
    },
  };
  </script>
  
  <style scoped>
  /* Add your styles here */
  </style>
  