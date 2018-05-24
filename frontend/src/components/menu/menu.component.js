import template from './menu.html';
import styles from './menu.scss';
import { MENU_ENTRIES } from './nav';

const UI_STRINGS = {
  profile: {
    changePassword: 'Change Password',
    logout: 'Logout',
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
      this.menuEntries = MENU_ENTRIES.filter(me => this.userHasOption(me.roles));
      this.userRole = this.user.roles[0].name || '';
    }

    isAdmin() {
      return this.user && this.user.role.name === 'admin';
    }

    userHasOption(roles) {
      if (!roles) return true;
      return roles.some(val => !!this.user.roles.find(r => r.name === val), true);
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

