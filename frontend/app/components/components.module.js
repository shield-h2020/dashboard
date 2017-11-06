import angular from 'angular';
import uiRouter from '@uirouter/angularjs';
import { MenuModule } from './menu/menu.module';
import { LoginModule } from './login/login.module';
import { HomeModule } from './home/home.module';
import { InputModule } from './input/input.module';
// import { ModalBoxModule } from './modal-box/modalbox.module';
import { UploadBoxModule } from './upload-box/uploadbox.module';
import { TableModule } from './table/table.module';
import { UtilitiesModule } from './utilities/utilities.module';
import { JsonViewerModule } from './json-viewer/json-viewer.module';
import { IncidentsModule } from './incidents/incidents.module';
import { VNSFModule } from './vnsfs/vnsf.module';
import { ModalModule } from './modal/modal.module';

export const ComponentsModule = angular.module('root.components', [
  MenuModule,
  LoginModule,
  HomeModule,
  InputModule,
  // ModalBoxModule,
  UploadBoxModule,
  uiRouter,
  TableModule,
  UtilitiesModule,
  JsonViewerModule,
  IncidentsModule,
  VNSFModule,
  ModalModule,
])
  .name;

export default ComponentsModule;
