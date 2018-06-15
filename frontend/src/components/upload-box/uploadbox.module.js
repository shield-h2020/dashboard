import angular from 'angular';
import { UploadBoxComponent } from './uploadbox.component';
import { FileUploader } from './file-uploader.directive';
import { FileOnChange } from './fileonchange.directive';
import { FileUploadService } from '../../services/fileupload.service';

export const UploadBoxModule = angular.module('file-uploader', [])
    .component('snUploadBox', UploadBoxComponent)
    .directive('snFileUploader', FileUploader)
    .directive('fileOnChange', FileOnChange)
    .service('FileUploadService', FileUploadService)
    .name;

export default UploadBoxModule;
