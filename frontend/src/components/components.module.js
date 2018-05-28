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
import { ModalModule } from './modal2/modal.module';
import { NSModule } from './nss/ns.module';
import { FooterModule } from './footer/footer.module';
import { UsersModule } from './users/users.module';
import { TenantsModule } from './tenants/tenants.module';
import { CatalogueModule } from './catalogue/catalogue.module';
import { OnboardValidationModule } from './onboard-validation/onboard-validation.module';
import { InventoryModule } from './inventory/inventory.module';
import Table2Module from './table2/table.module';

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
  NSModule,
  FooterModule,
  UsersModule,
  TenantsModule,
  Table2Module,
  CatalogueModule,
  OnboardValidationModule,
  InventoryModule,
])
  .name;

export default ComponentsModule;
