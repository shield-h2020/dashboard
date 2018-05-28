import template from './app.html';
import './app.scss';

export const AppComponent = {
  template,
};

export const appAbsState = {
  name: 'shield',
  url: '/shield',
  template: '<ui-view></ui-view>',
  abstract: true,
  resolve: {
    resolvedUser: ['AuthService', AuthService => AuthService.checkForAuthenticatedUser()],
  },
};

export const homeState = {
  parent: 'shield',
  name: 'home',
  url: '/home',
  component: 'homeView',
  resolve: {
    userdata: ['resolvedUser', resolvedUser => resolvedUser],
  },
};


export default AppComponent;
