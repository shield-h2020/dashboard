import template from './areainput.html';

export const AreaInputComponent = {

  template,
  bindings: {
    fieldValue: '<?',
    fieldLabel: '@?',
    fieldRows: '@?',
    onUpdate: '&',
  },
  controller: class AreaInput {

    change() {
      this.onUpdate({ $event: { value: this.fieldValue } });
    }
  },
};

export default AreaInputComponent;
