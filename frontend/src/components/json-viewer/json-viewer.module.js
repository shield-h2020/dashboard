import angular from 'angular';
import { JsonViewerComponent } from './json-viewer.component';

export const JsonViewerModule = angular.module('jsonViewer', ['ui.router'])
  .component('jsonViewer', JsonViewerComponent)
  .name;

export default JsonViewerModule;
