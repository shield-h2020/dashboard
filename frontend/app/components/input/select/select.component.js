import template from './select.html';
import styles from './select.scss';

export const SelectComponent = {
  template,
  bindings: {
    label: '<',
    compact: '<',
    options: '<',
    selected: '<?',
    onChange: '&',
  },
  controller: class SelectComponent {
    constructor() {
      this.styles = styles;
      this.firstSet = true;
    }

    $onInit() {
      if (!this.compact) this.compact = false;
      if (this.options.length) this.selected = this.options[0].value;
    }

    $onChanges(cObj) {
      if (cObj.options && cObj.options.currentValue.length) {
        this.selected = this.options[0].value;
        if (this.firstSet) {
          this.firstSet = false;
        } else {
          this.change();
        }
      }
    }

    change() {
      this.onChange({ $event: { value: this.selected } });
    }
  },
};

export default SelectComponent;
