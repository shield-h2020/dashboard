import angular from 'angular';
import { FileUploaderComponent } from './file-uploader.component';
import { FileUploaderDirective } from './file-uploader.directive';

export const FileUploaderModule = angular.module('fileUploader', [])
  .component('snFileUploader', FileUploaderComponent)
  .directive('fileUploadChange', FileUploaderDirective)
  .name;

export default FileUploaderModule;

