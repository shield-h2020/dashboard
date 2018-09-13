import { API_ADDRESS } from 'api/api-config';

export class DashboardService {
  constructor($http, $window, $httpParamSerializer, $q, toastr, AuthService, TenantsService, ErrorHandleService) {
    'ngInject';

    this.q = $q;
    this.http = $http;
    this.window = $window;
    this.httpParamSerializer = $httpParamSerializer;
    this.toast = toastr;
    this.authService = AuthService;
    this.tenantsService = TenantsService;
    this.errorHandleService = ErrorHandleService;
    this.infUsername = 'dashboard-admin';
    this.infPassword = 'st@ong_p@assw@ord!';
  }

  getTotalAttacks(startTime, endTime, tenant) {
    let url = `http://192.168.1.3:8086/query?db=cyberattack&q=SELECT COUNT("duration") FROM "attack" WHERE time > '${startTime}' AND time < '${endTime}' GROUP BY attack_type`;
    if (tenant) {
      url = `http://192.168.1.3:8086/query?db=cyberattack&q=SELECT COUNT("duration") FROM "attack" WHERE time > '${startTime}' AND time < '${endTime}' AND tenant = '${tenant}' GROUP BY attack_type`;
    }

    return this.http.get(
      url, {
        headers: {
          Authorization: `Basic ${this.window.btoa(`${this.infUsername}:${this.infPassword}`)}`,
          'Content-Type': 'application/json',
        },
      });
  }

  getTotalAttacksByDay(startTime, endTime, period, tenant) {
    let url = `http://192.168.1.3:8086/query?db=cyberattack&q=SELECT COUNT("duration") FROM "attack" WHERE time > '${startTime}' AND time < '${endTime}' GROUP BY ${period},attack_type`;
    if (tenant) {
      url = `http://192.168.1.3:8086/query?db=cyberattack&q=SELECT COUNT("duration") FROM "attack" WHERE time > '${startTime}' AND time < '${endTime}' AND tenant = '${tenant}' GROUP BY ${period},attack_type`;
    }

    return this.http.get(
      url, {
        headers: {
          Authorization: `Basic ${this.window.btoa(`${this.infUsername}:${this.infPassword}`)}`,
          'Content-Type': 'application/json',
        },
      });
  }

  getAttack(startTime, endTime, tenant, attack, page) {
    let url = `http://192.168.1.3:8086/query?db=cyberattack&q=SELECT * FROM "attack" WHERE time > '${startTime}' AND time < '${endTime}'`;
    if (tenant) {
      url += ` AND tenant = '${tenant}'`;
    }

    if (attack) {
      url += ` AND attack_type = '${attack}'`;
    }

    url += ` LIMIT 10 OFFSET ${page}`;

    return this.http.get(
      url, {
        headers: {
          Authorization: `Basic ${this.window.btoa(`${this.infUsername}:${this.infPassword}`)}`,
          'Content-Type': 'application/json',
        },
      });
  }

}

export default DashboardService;
