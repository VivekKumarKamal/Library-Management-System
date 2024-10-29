import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";
import LoginPage from "../views/LoginPage.vue";
import HomePage from "@/views/HomePage.vue";
import RegisterPage from "@/views/RegisterPage.vue";
import NewBookPage from "@/views/NewBookPage.vue";
import NewSectionPage from "@/views/NewSectionPage.vue";  
import EditEbookPage from "../views/EditEbookPage.vue";
import EditSectionPage from "../views/EditSectionPage.vue";
import BookPage from "../views/BookPage.vue";
import LibrarianDashboard from "@/views/LibrarianDashboard.vue";
import UserDashboard from "@/views/UserDashboard.vue";
import SearchPage from '@/views/SearchPage.vue';
import EditProfilePage from '@/views/EditProfilePage.vue';
import { requiresUser, requiresLibrarian } from '@/auth';

const routes = [
  {
    path: "/",
    name: "home",
    component: HomePage,
  },
  {
    path: "/login",
    name: "login",
    component: LoginPage,
  },
  {
    path: "/register",
    name: "register",
    component: RegisterPage,
  },
  {
    path: "/add-book",
    name: "add-book",
    component: NewBookPage,
  },
  {
    path: "/add-section",
    name: "add-section",
    component: NewSectionPage,
  },
  {
    path: "/edit-book/:id",
    name: "edit-book",
    props: true,
    meta: { requiresLibrarian: true },
    component: EditEbookPage,
  },  
  {
    path: "/edit-section/:id",
    name: "edit-section",
    props: true,
    meta: { requiresLibrarian: true },
    component: EditSectionPage,
  },
  {
    path: "/book/:id",
    name: "book",
    props: true,
    component: BookPage,
  },
  {
    path: "/librarian-dashboard",
    name: "librarian-dashboard",
    meta: { requiresLibrarian: true },
    component: LibrarianDashboard,
    beforeEnter: requiresLibrarian
  },
  {
    path: "/user-dashboard",
    name: "user-dashboard",
    meta: { requiresUser: true },
    component: UserDashboard,
    beforeEnter: requiresUser
  },
  {
    path: '/search',
    name: 'search',
    component: SearchPage
  },
  {
    path: '/edit-profile',
    name: 'EditProfile',
    component: EditProfilePage,
    meta: { requiresAuth: true }
  }
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;