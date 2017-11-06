import template from './menu.html';
import styles from './menu.scss';

export const UI_STRINGS = {
  labels: {
    global: 'Global options',
  },
  user: {
    main: [
      { label: 'Security Incidents', route: 'incidentslist' },
      { label: 'VNSFs Store', route: 'vnsfslist' },
    ],
  },
};

export const MenuComponent = {

  template,
  bindings: {
    user: '<',
  },
  controller: class MenuComponent {
    constructor($state, AuthService) {
      'ngInject';

      this.state = $state;
      this.authService = AuthService;
      this.user = {};
      this.strings = UI_STRINGS;
      this.styles = styles;
      this.mainOptions = [];
      this.globalOptions = [];
      // this.globalLabel = UI_STRINGS.labels.global;
      this.catalogue = [];
      this.isOpen = false;
      this.userOptionsOpen = false;
    }

    $onInit() {
      if (this.isAdmin()) {
        this.mainOptions.push(...UI_STRINGS.admin.main);
        // this.globalOptions.push(...UI_STRINGS.admin.global);
        this.catalogue = UI_STRINGS.admin.catalogue;
      } else {
        this.mainOptions.push(...UI_STRINGS.user.main);
      }
    }

    isAdmin() {
      return this.user && this.user.role.name === 'admin';
    }

    toggleSubMenu() {
      this.isOpen = !this.isOpen;
    }

    toggleUserOptions() {
      this.userOptionsOpen = !this.userOptionsOpen;
    }

    logout() {
      this.authService.logout();
    }
  },
};

export default MenuComponent;

