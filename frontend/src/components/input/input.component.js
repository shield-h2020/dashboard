import template from './input.html';

export const InputComponent = {
  template,
  bindings: {
    fieldType: '@',
    fieldLabel: '@?',
    placeholder: '@?',
    fieldValue: '<?',
    onUpdate: '&',
    fieldDisabled: '<?',
  },
  controller: class InputComponent {

    $onInit() {
      if (!this.fieldType) {
        this.fieldType = 'text';
      }
      if (!this.fieldValue) {
        this.fieldValue = '';
      }
      if (this.fieldDisabled === undefined) {
        this.fieldDisabled = false;
      }
    }

    change() {
      this.onUpdate({ $event: { value: this.fieldValue } });
    }

  },
};

export default InputComponent;
