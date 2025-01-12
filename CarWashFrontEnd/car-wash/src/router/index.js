import { createRouter, createWebHistory } from 'vue-router';
import Cookies from 'js-cookie'; 

import Auth from '../views/authentication.vue';
import Login from '../views/login.vue';
import UserSignup from '../views/signup-user.vue';
import WorkerSignup from '../views/signup-worker.vue';
import VerifyPhone from '../views/verify-phone.vue';
import VerifyCode from '../views/verify-code.vue';
import NewPassword from '../views/new-password.vue';
import Home from '../views/home.vue';
import AboutUs from '../views/about-us.vue';
import ContactUs from '../views/contact-us.vue';
import Services from '../views/services.vue';
import Dashboard from '../views/dashboard.vue';
import Service from '../views/service.vue';
import Order from '../views/order.vue';
import Reports from '../views/reports.vue';

const routes = [
  { path: '/', name: 'home', component: Home },
  {
    path: '/dashboard',
    name: 'dashboard',
    component: Dashboard,
    meta: { isProtected: true },
  },
  { path: '/about-us', name: 'about-us', component: AboutUs },
  { path: '/contact-us', name: 'contact-us', component: ContactUs },
  { path: '/services', name: 'services', component: Services },
  { path: '/reports', name: 'reports', component: Reports },
  { path: '/service/:slug', name: 'service', component: Service },
  {
    path: '/order/:slug',
    name: 'order',
    component: Order,
    props: true,
  },
  {
    path: '/authentication',
    name: 'authentication',
    redirect: '/authentication/login',
    component: Auth,
    meta: { isAuthenticate: true },
    children: [
      { path: 'login', name: 'login', component: Login },
      { path: 'user-signup', name: 'user-signup', component: UserSignup },
      { path: 'worker-signup', name: 'worker-signup', component: WorkerSignup },
      { path: 'forgetpassword/verify-phone', name: 'verifyphone', component: VerifyPhone },
      { path: 'forgetpassword/verify-code', name: 'verifycode', component: VerifyCode },
      { path: 'forgetpassword/new-password', name: 'newpassword', component: NewPassword },
    ],
  },
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
});

router.beforeEach((to, from, next) => {
  const { isProtected, isAuthenticate } = to.meta;

  if (to.path.startsWith('/order') && from.path === '/') {
    return next('/services');
  }

  if (isProtected && !Cookies.get('token')) {
    return next('/authentication/login');
  } else if (isAuthenticate && Cookies.get('token')) {
    return next('/');
  }

  next();
});

export default router;
