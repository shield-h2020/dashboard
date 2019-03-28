import { AUTH_ADDRESS } from 'api/api-config';

const AUTH_API = '/login';

export class AuthService {

  constructor($http, $window, $q, $state) {
    'ngInject';

    this.http = $http;
    this.window = $window;
    this.q = $q;
    this.state = $state;
  }

  login(username, password, scope) {
    console.log(AUTH_ADDRESS + AUTH_API);
    return this.http.post(AUTH_ADDRESS + AUTH_API, {}, {
      headers: {
        Authorization: `Basic ${this.window.btoa(`${username}:${password}`)}`,
        'Shield-Authz-Scope': scope,
        'Content-Type': 'application/json',
      },
    })
      .then((response) => {
        const token = response.data.token;
        if (token) {
          this.storeSessionInfo(token.id, AuthService.formatSession(token));
          this.http.defaults.headers.common.Authorization = `Basic ${this.window.btoa(`${token.id}:''`)}`;
          this.state.go('home');
        }
      });
  }

  logout() {
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
    return this.q((resolve, reject) => {
      if (currentSession.session) {
        this.http.defaults.headers.common.Authorization = `Basic ${this.window.btoa(`${currentSession.token}:''`)}`;
        resolve(currentSession.session);
      } else {
        reject('NO USER');
      }
    });
  }

  isUserPlatformAdmin() {
    const user = this.getSessionInfo();
    return !!user.session.roles.find(r => r.name === 'admin');
  }

  isUserTenantAdmin() {
    const user = this.getSessionInfo();
    return !!user.session.roles.find(r => r.name === 'shield_client_admin');
  }

  isUserDeveloper() {
    const user = this.getSessionInfo();
    return !!user.session.roles.find(r => r.name === 'shield_developer');
  }
  isUserCyberAgent() {
    const user = this.getSessionInfo();
    return !!user.session.roles.find(r => r.name === 'shield_cyberagent');
  }

  getTenant() {
    return this.getSessionInfo().session.user.domain.id;
  }

  getTenantName() {
    return this.getSessionInfo().session.user.domain.name;
  }

  static formatSession(session) {
    const { roles, user } = session;
    return {
      user,
      roles,
    };
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
