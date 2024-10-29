<template>
    <div class="container mt-5">
      <div class="row justify-content-center">
        <div class="col-md-6">
          <div class="card">
            <div class="card-header bg-dark text-white">
              <h3 class="text-center">Sign Up</h3>
            </div>
            <div class="card-body">
              <form @submit.prevent="register">
                <div class="mb-3 row">
                  <label for="name" class="col-sm-4 col-form-label text-end"
                    >Name</label
                  >
                  <div class="col-sm-8">
                    <input
                      type="text"
                      class="form-control"
                      id="name"
                      v-model="name"
                      required
                    />
                  </div>
                </div>
                <div class="mb-3 row">
                  <label for="email" class="col-sm-4 col-form-label text-end"
                    >Email address</label
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
                <div class="mb-3 row">
                  <label
                    for="confirmPassword"
                    class="col-sm-4 col-form-label text-end"
                    >Confirm Password</label
                  >
                  <div class="col-sm-8">
                    <input
                      type="password"
                      class="form-control"
                      id="confirmPassword"
                      v-model="confirmPassword"
                      required
                    />
                  </div>
                </div>
                <button type="submit" class="btn btn-primary w-100">
                  Register
                </button>
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
    name: "SignupPage",
    data() {
      return {
        name: "",
        email: "",
        password: "",
        confirmPassword: "",
      };
    },
    methods: {
      async register() {
        if (this.password !== this.confirmPassword) {
          alert("Passwords don't match");
          return;
        }
  
        try {
          const response = await axios.post("http://localhost:5000/register", {
            name: this.name,
            email: this.email,
            password: this.password,
          });
  
          if (response.status === 201) {
            alert("User registered successfully");
            this.$router.push("/login");
          }
        } catch (error) {
          if (error.response && error.response.data) {
            alert(error.response.data.message);
          } else {
            alert("An error occurred during registration");
          }
        }
      },
    },
  };
  </script>
  