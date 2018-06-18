import template from './list-input.html';
import styles from './list-input.scss';

const VIEW_STRINGS = {
  placeholder: 'Type and press enter...',
};

export const ListInputComponent = {
  template,
  bindings: {
    items: '<',
    onChange: '&',
    label: '@',
    id: '@',
    validator: '<?',
  },
  controller: class ListInputComponent {
    constructor() {
      this.viewStrings = VIEW_STRINGS;
      this.styles = styles;
      this.currInput = '';
    }

    $onInit() {
      if (this.items) {
        this.innerItems = [...this.items];
      }
    }

    $onChanges(changesObj) {
      if (changesObj.items && changesObj.items.currentValue) {
        this.innerItems = [...changesObj.items.currentValue];
      }

      if (changesObj.open && !changesObj.open.currentValue) {
        this.currInput = '';
      }
    }

    onKeypress(event) {
      const keyCode = event.which || event.keyCode;
      if (keyCode === 13) {
        if (this.innerItems.indexOf(this.currInput) === -1) {
          this.validateAndAddToList();
        }
      }
    }

    validateAndAddToList() {
      const valid = this.validator ? this.validator(this.currInput) : true;
      valid && this.addToList();
    }

    addToList() {
      this.innerItems.push(this.currInput);
      this.change();
      this.currInput = '';
    }

    removeFromList(item) {
      const idx = this.innerItems.indexOf(item);

      if (idx > -1) {
        this.innerItems.splice(idx, 1);
      }

      this.change();
    }

    change() {
      this.onChange({ $event: { value: this.innerItems } });
    }
  },
};

export default ListInputComponent;
