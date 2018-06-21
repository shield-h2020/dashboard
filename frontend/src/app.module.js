import angular from 'angular';
import toastr from 'angular-toastr';
import uiRouter from '@uirouter/angularjs';
import { AuthService } from './services/auth.service';
import { AppComponent, appAbsState, homeState } from './app.component';
import { ComponentsModule } from 'components/components.module';
import { INTERNAL_ERROR_MODAL_EVENT } from 'components/modal-box/internal-error/internal-error.component';

import './styles/main.global.scss';
import '../node_modules/angular-toastr/dist/angular-toastr.css';
import '../node_modules/spaaace/dist/style.css';

export const AppModule = angular
    .module('root', [
      ComponentsModule,
      uiRouter,
      toastr,
    ])
    .component('root', AppComponent)
    .service('AuthService', AuthService)
    .config(($stateProvider, $urlServiceProvider) => {
      'ngInject';

      // $locationProvider.html5Mode(true);
      $urlServiceProvider.rules.otherwise({ state: 'home' });

      $stateProvider
        .state(appAbsState)
        .state(homeState);
    })
    .config(($httpProvider) => {
      'ngInject';

      $httpProvider.interceptors.push(($state, $q, $rootScope) => {
        'ngInject';

        return {
          responseError(response) {
            if (response.status === 401) {
              $state.go('login');
            } else if (response.data && response.data.code === '205') {
              $rootScope.$broadcast(INTERNAL_ERROR_MODAL_EVENT.CAST.OPEN, response.data);
            }

            return $q.reject(response);
          },
        };
      });
    })
    .config((toastrConfig) => {
      'ngInject';

      angular.extend(toastrConfig, {
        timeOut: 3000,
      });
    })
    .name;

export default AppModule;
