import template from './search-input.html';
import styles from './search-input.scss';

const UI_STRINGS = {
  PLACEHOLDER: 'Start typing to search…',
};

export const SearchInputComponent = {
  template,
  bindings: {
    onChange: '&',
  },
  controller: class SearchInputComponent {
    constructor() {
      this.strings = UI_STRINGS;
      this.styles = styles;
      this.searched = '';
    }

    change() {
      this.onChange({ $event: { value: this.searched } });
    }
  },
};

export default SearchInputComponent;
