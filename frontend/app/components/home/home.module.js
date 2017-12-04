import angular from 'angular';
import { HomeComponent } from './home.component';

export const HomeModule = angular.module('home', [])
    .component('homeView', HomeComponent)
    .name;

export default HomeModule;
