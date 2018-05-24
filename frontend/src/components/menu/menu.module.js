import angular from 'angular';
import { MenuComponent } from './menu.component';

export const MenuModule = angular.module('menu', ['ui.router'])
    .component('snMenu', MenuComponent)
    .name;

export default MenuModule;
