import template from './selectinput.html';

export const SelectInputComponent = {

  template,
  bindings: {
    fieldLabel: '@',
    selected: '<?',
    options: '<',
    onUpdate: '&',
  },
  controller: class SelectInputComponent {

    $onInit() {
      this.setOptions(this.options, true);
    }

    $onChanges(changes) {
      if (changes.options) {
        this.setOptions(changes.options.currentValue);
      }
    }

    setOptions(options, isInit) {
      if (options) {
        const opt = options.find(option => option.value === this.selected);
        if (opt) {
          this.currentValue = opt;
        } else if (isInit && options.length > 0) {
          this.currentValue = this.options[0];
        }
      }
    }

    changed(option) {
      this.onUpdate({
        $event: {
          value: option,
        },
      });
    }
  },

};

export default SelectInputComponent;
