import angular from 'angular';
import { LoginComponent, loginState } from './login.component';

export const LoginModule = angular.module('login', [])
  .component('loginView', LoginComponent)
  .config(($stateProvider) => {
    'ngInject';

    $stateProvider
    .state(loginState);
  })
  .name;

export default LoginModule;
