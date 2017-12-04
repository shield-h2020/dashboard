import { API_STRINGS, APP_ADDRESSES } from '../strings/api-strings';

export class AuthService {

  constructor($http, $window, $q, $state) {
    'ngInject';

    this.http = $http;
    this.window = $window;
    this.q = $q;
    this.state = $state;
  }

  login(username, password, tenant) {
    return this.http.post(APP_ADDRESSES.authAddress + API_STRINGS.auth.base,
      {
        auth: {
          username,
          password,
          tenant,
        },
      })
    .then((response) => {
      const token = response.headers('x-subject-token');
      this.storeSessionInfo(token, response.data.session);
      this.http.defaults.headers.common['X-Auth-Token'] = token;

      return response;
    });
  }

  logout() {
    delete this.http.defaults.headers.common['X-Auth-Token'];
    this.deleteSessionInfo();
    this.state.go('login');
  }

  checkForAuthenticatedUser() {
    return this.getCurrentUser()
      .then(user => user)
      .catch(() => { this.state.go('login'); });
  }

  getCurrentUser() {
    const currentSession = this.getSessionInfo();
    if (currentSession.session) {
      this.http.defaults.headers.common['X-Auth-Token'] = currentSession.token;
      return this.q.when(currentSession.session.user);
    }
    return this.q.reject('NO USER');
  }

  storeSessionInfo(token, session) {
    this.window.sessionStorage.setItem('session', JSON.stringify(session));
    this.window.sessionStorage.setItem('token', token);
  }

  getSessionInfo() {
    return {
      token: this.window.sessionStorage.getItem('token'),
      session: JSON.parse(this.window.sessionStorage.getItem('session')),
    };
  }

  storeCurrentState(state) {
    this.window.sessionStorage.setItem('laststate', state);
  }

  getLastState() {
    return this.window.sessionStorage.getItem('laststate');
  }

  deleteSessionInfo() {
    this.window.sessionStorage.removeItem('laststate');
    this.window.sessionStorage.removeItem('token');
    this.window.sessionStorage.removeItem('session');
  }
}

export default AuthService;
