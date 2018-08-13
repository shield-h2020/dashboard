import angular from 'angular';
import { DashViewerDirective } from './dash-viewer.directive';

export const DashViewerModule = angular.module('dashViewer', [])
    // .component('svViewer', ViewerComponent)
    .directive('dashViewer', DashViewerDirective)
    .name;

export default DashViewerModule;
