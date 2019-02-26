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
import { VNSFCatalogueModule } from './vnsfs-catalogue/vnsfs-catalogue.module';
import { ModalModule } from './modal2/modal.module';
import { FooterModule } from './footer/footer.module';
import { UsersModule } from './users/users.module';
import { DashboardModule } from './dashboard/dashboard.module';
import { AttestationModule } from './attestation/attestation.module';
import { AttestationHistoryModule } from './attestation-history/attestation-history.module';
import { TenantsModule } from './tenants/tenants.module';
import { CatalogueModule } from './catalogue/catalogue.module';
import { BillingModule } from './billing/billing.module';
import { BillingDetailModule } from './billing-detail/billing-detail.module';
import { OnboardValidationModule } from './onboard-validation/onboard-validation.module';
import { NsInventoryModule } from './ns-inventory/ns-inventory.module';
import { NsInstancesModule } from './ns-instances/ns-instances.module';
import { VnsfNotificationsModule } from './vnsf-notifications/vnsf-notifications.module';

import Table2Module from './table2/table.module';
import TableCustomActionsModule from './table-custom-actions/table-custom-actions.module';

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
  VNSFCatalogueModule,
  ModalModule,
  FooterModule,
  UsersModule,
  DashboardModule,
  AttestationModule,
  AttestationHistoryModule,
  TenantsModule,
  Table2Module,
  TableCustomActionsModule,
  CatalogueModule,
  BillingModule,
  BillingDetailModule,
  OnboardValidationModule,
  NsInventoryModule,
  NsInstancesModule,
  VnsfNotificationsModule,
])
  .name;

export default ComponentsModule;
