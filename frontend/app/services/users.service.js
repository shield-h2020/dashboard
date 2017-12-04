import { API_STRINGS, APP_ADDRESSES, ACCESSORS } from '../strings/api-strings';

export class UsersService {
  constructor($http, $state, AuthService, toastr) {
    'ngInject';

    this.http = $http;
    this.state = $state;
    this.authService = AuthService;
    this.toast = toastr;
  }

  getAllUsers(tenantID) {
    let id = tenantID;
    if (!id) {
      id = this.authService.getSessionInfo().session.user.tenant.id;
    }
    return this.http.get(APP_ADDRESSES.baseAddress + API_STRINGS.users.all
      .replace(ACCESSORS.id, tenantID))
      .then(response => response.data.users)
      .catch(() => {
        this.toast.error('An error occurred');
      });
  }

  getUser(tenantID, userId) {
    let tid = tenantID;
    if (!tid) {
      tid = this.authService.getSessionInfo().session.user.tenant.id;
    }
    return this.http.get(APP_ADDRESSES.baseAddress + API_STRINGS.users.one
      .replace(ACCESSORS.id, tenantID)
      .replace(ACCESSORS.nId, userId))
      .then(response => response.data.user)
      .catch(() => {
        this.toast.error('An error occurred');
      });
  }

  createUser(tenantId, user) {
    return this.http.post(APP_ADDRESSES.baseAddress + API_STRINGS.users.all
      .replace(ACCESSORS.id, tenantId), { user })
      .then((response) => {
        this.toast.success('User created', 'Success');
        return response.data.user;
      })
      .catch(() => {
        this.toast.error('An error occurred');
      });
  }

  updateUser(tenantId, user) {
    return this.http.patch(APP_ADDRESSES.baseAddress + API_STRINGS.users.one
      .replace(ACCESSORS.id, tenantId)
      .replace(ACCESSORS.nId, user.id), { user })
      .then((response) => {
        this.toast.info('User updated');
        return response.data.user;
      })
      .catch(() => {
        this.toast.error('An error occurred');
      });
  }

  deleteUser(tenantId, userId) {
    return this.http.delete(APP_ADDRESSES.baseAddress + API_STRINGS.users.one
      .replace(ACCESSORS.id, tenantId)
      .replace(ACCESSORS.nId, userId))
      .then(() => {
        this.toast.info('User deleted');
      })
      .catch(() => {
        this.toast.error('An error occurred');
      });
  }
}

export default UsersService;
