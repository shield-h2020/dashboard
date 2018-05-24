import template from './login.html';
import styles from './login.scss';

export const UI_STRINGS = {
  username: 'username',
  password: 'password',
  domain: 'client',
  login: 'login',
  error: 'Incorrect username or password. Please review your information and try again.',
};


export const LoginComponent = {

  template,
  controller: class LoginComponent {

    constructor(AuthService, $state) {
      'ngInject';

      this.states = $state;
      this.strings = UI_STRINGS;
      this.auth = AuthService;
      this.styles = styles;
      this.username = '';
      this.password = '';
      this.domain = '';
      this.errorSubmitted = false;
      this.isChecking = false;
    }

    login(isValid) {
      this.errorSubmitted = false;
      if (isValid) {
        this.isChecking = true;
        this.auth.login(this.username, this.password, this.domain)
          .then((response) => {
            if (response.status === 201) {
              this.states.go('home');
            } else if (response.status === 401) {
              this.errorSubmitted = true;
              this.isChecking = false;
            }
          })
          .catch(() => {
            this.errorSubmitted = true;
            this.isChecking = false;
          });
      }
    }
  },
};

export const loginState = {
  name: 'login',
  url: '/login',
  component: 'loginView',
};

export default LoginComponent;
