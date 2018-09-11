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

    getTotalAttacks(startTime, endTime) {
      console.log("Here we go");
      return this.http.get(`http://127.0.0.1:8086/query?q=SELECT COUNT("duration") as attacks FROM "attack" WHERE time > '2017-10-24T00:00:00.000Z' AND time < '2018-10-25T00:00:00.000Z' GROUP BY "attack_type"&db=cyberattack`, {
          headers: {
            Authorization: `Basic ${this.window.btoa(`${this.infUsername}:${this.infPassword}`)}`,
            //Authorization: `Basic ZGFzaGJvYXJkLWFkbWluOnN0QG9uZ19wQGFzc3dAb3JkIQ==`,
            'Content-Type': 'application/json',
            
          },
        })
        .then((response) => {
          
          const _items = response.data.results[0].series;
          return {
            items: _items.map(item => ({
              ...item,
              type: item.tags.attack_type,
              total: item.values[0][1]
              }))
          };
        })
        .catch(function(e){console.log("Error getting influxData (1)");});
    }

    getTotalAttacksByDay(startTime, endTime) {

      return this.http.get(`http://127.0.0.1:8086/query?q=SELECT COUNT("duration") as attacks FROM "attack" WHERE time > '2017-10-24T00:00:00.000Z' AND time < '2018-10-25T00:00:00.000Z' GROUP BY "attack_type", time(1d)&db=cyberattack`, {
          headers: {
            Authorization: `Basic ${this.window.btoa(`${this.infUsername}:${this.infPassword}`)}`,
            //Authorization: `Basic ZGFzaGJvYXJkLWFkbWluOnN0QG9uZ19wQGFzc3dAb3JkIQ==`,
            'Content-Type': 'application/json',
            
          },
        })
        .then((response) => {
          
          const _items = response.data.results[0].series;
          return {
            items: _items.map(item => ({
              ...item,
              type: item.tags.attack_type
              }))
          };
        })
        .catch(function(e){console.log("Error getting influxData (2)");});
    }

}
export default DashboardService;