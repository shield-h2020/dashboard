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

      this.state = $state;
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
      const goTo = this.state.params.prevRoute || 'home';
      console.log(goTo)
      this.errorSubmitted = false;
      if (isValid) {
        this.isChecking = true;
        this.auth.login(this.username, this.password, this.domain)
          .then((response) => {
            if (response.status === 201) {
              this.state.go(goTo);
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
  params: {
    prevRoute: null,
  },
};

export default LoginComponent;
