import angular from 'angular';
import { UsersListComponent, UsersListState } from './users-list/users-list.component';
import { UsersService } from './users.service';

export const UsersModule = angular.module('users', ['ui.router'])
  .component('usersListView', UsersListComponent)
  .service('UsersService', UsersService)
  .config(($stateProvider) => {
    'ngInject';

    $stateProvider.state(UsersListState);
  })
  .name;

export default UsersModule;
