import template from './onboard-validation.html';

const VIEW_STRING = {
  title: 'Onboard validation',
};

export const OnboardValidationComponent = {
  template,
  controller: class OnboardValidationComponent {
    constructor($stateParams, $state, $scope, OnboardValidationService) {
      'ngInject';

      this.scope = $scope;
      this.stateParams = $stateParams;
      this.state = $state;
      this.validationService = OnboardValidationService;
      this.viewStrings = VIEW_STRING;
    }

    $onInit() {
      this.validationService.getResults(this.stateParams.validation)
        .then((obj) => {
          this.errCount = obj.errors;
          this.warnCount = obj.warnings;
          this.scope.errors = obj.issues.filter(i => i.level === 'error');
          this.scope.warnings = obj.issues.filter(i => i.level === 'warning');
        });
      this.validationService.getValidation(this.stateParams.validation)
        .then((obj) => {
          if (obj.nodes.length || obj.links.length) {
            this.scope.topology = obj;
          }
        });
    }

    $onChanges(changesObj) {
      if (changesObj.errors) {
        this.tmperrors = changesObj.errors.currentValue;
      }

      if (changesObj.warnings) {
        this.tmpwarnings = changesObj.warnings.currentValue;
      }
      if (changesObj.topology && changesObj.topology.currentValue) {
        this.isLoading = false;
        this.scope.topology = changesObj.topology.currentValue;
        this.scope.errors = this.tmperrors;
        this.scope.warnings = this.tmpwarnings;
        this.scope.isValid = true;
      } else if (changesObj.topology) {
        if (changesObj.topology.currentValue === null) {
          this.clearData();
        }
      }

      if (changesObj.fwgraphs && changesObj.fwgraphs.currentValue) {
        this.fwgraphs = changesObj.fwgraphs.currentValue;
        this.scope.fwgraph = this.fwgraphs[0];
      }
    }

    clearData() {
      this.scope.topology = null;
      this.fwgraphs.length = 0;
      this.scope.fwgraph = null;
    }


    static parseObject(obj, type) {
      const parsed = [];

      if (obj[type]) {
        obj[type].forEach((ele) => {
          const found = parsed.find(p => p.sourceId === ele.source_id);
          const details = [];
          ele.detail.forEach((det) => {
            details.push({
              eventId: det.detail_event_id,
              message: det.message,
            });
          });
          if (found) {
            found.events.push({
              eventCode: ele.event_code,
              eventId: ele.event_id,
              header: ele.header,
              details,
            });
          } else {
            const newObjectId = {
              sourceId: ele.source_id,
              events: [{
                eventCode: ele.event_code,
                eventId: ele.event_id,
                header: ele.header,
                details,
              }],
            };
            parsed.push(newObjectId);
          }
        });
      }

      return parsed;
    }
  },
};

export const validationState = {
  parent: 'home',
  name: 'validation',
  url: '/validation',
  component: 'validationView',
  params: {
    validation: null,
  },
};
